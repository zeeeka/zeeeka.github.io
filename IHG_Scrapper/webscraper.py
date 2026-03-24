import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🚀 Starting High-Endurance Session...")
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        context.set_default_timeout(300000) # 5 minutes
        page = await context.new_page()

        async def update_view(step_name):
            print(f"📸 Step: {step_name}")
            await page.screenshot(path="live_view.png")

        try:
            # --- INITIAL LOGIN STEPS ---
            await page.goto("https://apps.usw2.pure.cloud/directory/#", wait_until="networkidle")
            await page.get_by_text("More Login Options").click()
            
            await page.wait_for_selector("input[type='text']", state="visible")
            await page.fill("input[type='text']", "ihg")
            await page.keyboard.press("Enter")

            await page.wait_for_selector("img[alt='Ping Identity']", state="attached")
            await page.click("img[alt='Ping Identity']")
            
            await page.wait_for_selector("input[name='pf.username']", state="visible")
            await page.fill("input[name='pf.username']", "UOARTG")
            await page.fill("input[name='pf.pass']", "Welc0metp@2027")
            
            print("🚀 Clicking Login...")
            await page.click("text=/Login/i")

            # --- PING AUTHENTICATOR (MFA) STEP ---
            await update_view("Waiting for MFA")
            print("\n" + "!"*40)
            # This pauses the script and waits for YOUR input in the terminal
            mfa_code = input("👉 ENTER YOUR 6-DIGIT PING AUTHENTICATOR CODE: ")
            print("!"*40 + "\n")

            print(f"⌨️ Inputting MFA Code: {mfa_code}")
            # Target the only input field usually present on the MFA screen
            await page.wait_for_selector("input", state="visible")
            await page.fill("input", mfa_code)
            await page.keyboard.press("Enter")

            # --- THE "CHANGE IT LATER" BYPASS ---
            print("⏳ Checking for 'Change it later' link...")
            try:
                # Short timeout because this page might not always appear
                change_later = page.get_by_text("Change it later")
                await change_later.wait_for(state="visible", timeout=10000)
                await change_later.click()
                print("✅ Clicked 'Change it later'.")
            except:
                print("⚠️ 'Change it later' link not found or skipped.")

            # --- FINAL VALIDATION ---
            print("🔄 Loading Dashboard...")
            await page.wait_for_load_state("networkidle")
            await update_view("FINAL_DASHBOARD")
            
            print("\n" + "="*30 + " SUCCESS " + "="*30)
            print("You are now logged in. Check live_view.png.")
            # Print first 1000 chars of dashboard source
            content = await page.content()
            print(content[:1000]) 
            print("="*69)

        except Exception as e:
            print(f"❌ ERROR: {e}")
            await page.screenshot(path="error_state.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
