import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import os
import gc
import re

# --- 1. THE CLEANING FUNCTIONS ---

def clean_transcript(text):
    """
    Strips the header metadata, agent names, and timestamps.
    Leaves only the pure conversation text.
    """
    if not isinstance(text, str):
        return ""

    # Step A: Remove the Header Block
    text = re.sub(r'Interaction Type:.*?Date/Time\s+Participant Type\s+Participant Text', '', text, flags=re.DOTALL)

    # Step B: Remove Speaker Labels & Timestamps
    patterns_to_remove = [
        r'\d{2}:\d{2}\s+Internal\s+.*?(?=\s+‪|\s+[a-zA-ZäöüÄÖÜ])',
        r'\d{2}:\d{2}\s+External\s+.*?(?=\s+‪|\s+[a-zA-ZäöüÄÖÜ])',
        r'Internal\s+.*?(?=\s+‪)',
        r'External\s+.*?(?=\s+‪)',
        r'‪', 
        r'‬'
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text)

    # Step C: Final Polish
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_last_quarter(text):
    """Slices the last 25% to focus on the outcome."""
    start_index = int(len(text) * 0.75)
    return text[start_index:]

# --- 2. DATA UTILITIES ---

def load_and_preprocess_csv(file_path):
    try:
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin1', on_bad_lines='skip')
    
    # Grab last two columns (Transcript and Label) for training
    new_df = df.iloc[:, [-2, -1]].copy()
    new_df.columns = ['transcript', 'label']
    
    print("\n--- Cleaning & Pre-processing Training Data ---")
    new_df['transcript'] = new_df['transcript'].apply(clean_transcript)
    new_df['transcript'] = new_df['transcript'].apply(get_last_quarter)
    
    return new_df

# --- 3. TRAINING LOGIC ---

def train_booking_model(csv_path, model_save_path="./booking_classifier_model"):
    df = load_and_preprocess_csv(csv_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    model_name = "distilbert-base-multilingual-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    def tokenize_func(examples):
        return tokenizer(examples["transcript"], padding="max_length", truncation=True, max_length=128)

    tokenized_train = train_dataset.map(tokenize_func, batched=True)
    tokenized_test = test_dataset.map(tokenize_func, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",  
        learning_rate=3e-5,
        per_device_train_batch_size=1,        
        gradient_accumulation_steps=8,        
        num_train_epochs=3,
        weight_decay=0.01,
        fp16=False,
        logging_steps=1,
        save_total_limit=1,
        dataloader_pin_memory=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_test,
    )

    print("Training starting (German Multilingual Mode)...")
    gc.collect() 
    trainer.train()

    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    print(f"\nSUCCESS: Model saved to {model_save_path}")

# --- 4. INFERENCE LOGIC (The Prediction Addition) ---

def predict_on_new_file(input_csv, model_path="./booking_classifier_model", output_csv="final_predictions.csv"):
    print(f"\n--- Starting Prediction on: {input_csv} ---")
    
    if not os.path.exists(model_path):
        print("Error: Trained model folder not found!")
        return

    # Load Model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval()

    # Load Prediction Data
    try:
        df = pd.read_csv(input_csv, sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv(input_csv, sep=None, engine='python', encoding='latin1')

    # Column Mapping: ID (Col 0), Transcript (Col 1)
    ids = df.iloc[:, 0]
    raw_transcripts = df.iloc[:, 1]
    
    predictions = []

    print("Analyzing transcripts...")
    with torch.no_grad():
        for text in raw_transcripts:
            # Apply same cleaning as training
            cleaned = clean_transcript(str(text))
            processed = get_last_quarter(cleaned)
            
            inputs = tokenizer(processed, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
            outputs = model(**inputs)
            
            pred_id = torch.argmax(outputs.logits, dim=1).item()
            # Convert 0/1 to text
            label = "Booking" if pred_id == 1 else "No Booking"
            predictions.append(label)

    # Build the final CSV
    output_df = pd.DataFrame({
        'ID': ids,
        'Transcript': raw_transcripts,
        'Prediction': predictions
    })

    output_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f"SUCCESS: Result saved to {output_csv}")

# --- 5. RUN EVERYTHING ---

if __name__ == "__main__":
    # --- CHANGE THESE FILENAMES IF NEEDED ---
    TRAINING_DATA = "transcriptiondata.csv"
    FILE_TO_PREDICT = "to_predict.csv" 
    # ----------------------------------------

    if os.path.exists(TRAINING_DATA):
        try:
            # Phase 1: Train
            train_booking_model(TRAINING_DATA)
            
            # Phase 2: Predict
            if os.path.exists(FILE_TO_PREDICT):
                predict_on_new_file(FILE_TO_PREDICT)
            else:
                print(f"Note: '{FILE_TO_PREDICT}' not found. Skipping prediction phase.")
                
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print(f"Error: Could not find training file '{TRAINING_DATA}'.")
