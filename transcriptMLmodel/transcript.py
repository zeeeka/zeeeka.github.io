import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset
import os
import gc
import re

# --- 1. THE CLEANING FUNCTION ---

def clean_transcript(text):
    """
    Strips the header metadata, agent names, and timestamps.
    Leaves only the pure conversation text.
    """
    if not isinstance(text, str):
        return ""

    # Step A: Remove the Header Block
    # This removes everything from "Interaction Type" up to "Participant Text"
    text = re.sub(r'Interaction Type:.*?Date/Time\s+Participant Type\s+Participant Text', '', text, flags=re.DOTALL)

    # Step B: Remove Speaker Labels & Timestamps
    # Patterns to match: 00:07 Internal [Name], 00:14 External [Info]
    patterns_to_remove = [
        r'\d{2}:\d{2}\s+Internal\s+.*?(?=\s+‪|\s+[a-zA-ZäöüÄÖÜ])',
        r'\d{2}:\d{2}\s+External\s+.*?(?=\s+‪|\s+[a-zA-ZäöüÄÖÜ])',
        r'Internal\s+.*?(?=\s+‪)',
        r'External\s+.*?(?=\s+‪)',
        r'‪', # Special Unicode characters
        r'‬'
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, '', text)

    # Step C: Final Polish
    # Remove any lingering double spaces and strip edges
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# --- 2. DATA UTILITIES ---

def load_and_preprocess_csv(file_path):
    try:
        # Standardize loading for German Excel CSVs
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, sep=None, engine='python', encoding='latin1', on_bad_lines='skip')
    
    # Grab last two columns (Transcript and Label)
    new_df = df.iloc[:, [-2, -1]].copy()
    new_df.columns = ['transcript', 'label']
    
    print("\n--- Cleaning & Pre-processing ---")
    # 1. Clean the text (Remove headers/names)
    new_df['transcript'] = new_df['transcript'].apply(clean_transcript)
    
    # 2. Slice the last 25% (To focus on the outcome)
    def get_last_quarter(text):
        start_index = int(len(text) * 0.75)
        return text[start_index:]
    
    new_df['transcript'] = new_df['transcript'].apply(get_last_quarter)
    
    print("Cleaned Preview (Last 25%):")
    if not new_df.empty:
        print(new_df['transcript'].iloc[0][:150] + "...") 
    
    return new_df

# --- 3. TRAINING LOGIC (Low RAM Settings) ---

def train_booking_model(csv_path, model_save_path="./booking_classifier_model"):
    df = load_and_preprocess_csv(csv_path)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    # Multilingual model for German support
    model_name = "distilbert-base-multilingual-cased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    def tokenize_func(examples):
        # max_length=128 is a "safe zone" for Codespaces memory
        return tokenizer(examples["transcript"], padding="max_length", truncation=True, max_length=128)

    tokenized_train = train_dataset.map(tokenize_func, batched=True)
    tokenized_test = test_dataset.map(tokenize_func, batched=True)

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",  
        learning_rate=3e-5,
        per_device_train_batch_size=1,        # Minimal RAM usage
        gradient_accumulation_steps=8,        # Effectively batch size 8
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

if __name__ == "__main__":
    MY_CSV_FILE = "transcriptiondata.csv" # Ensure your file is named this or change it here
    if os.path.exists(MY_CSV_FILE):
        try:
            train_booking_model(MY_CSV_FILE)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Error: Could not find '{MY_CSV_FILE}'.")
