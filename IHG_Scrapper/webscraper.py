import asyncio
import os
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        print("🚀 Starting Full-Visibility Session...")
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        context.set_default_timeout(300000) 
        page = await context.new_page()

        async def update_view(step_name):
            """Saves a frame and prints to terminal so you can follow along"""
            print(f"📸 [LIVE VIEW UPDATE]: {step_name}")
            await page.screenshot(path="live_view.png")

        async def force_click_change_later(label):
            """Deep-Click logic with visibility update"""
            print(f"🔍 Searching for 'Change it later' ({label})...")
            clicked = await page.evaluate("""() => {
                const xpath = "//*[contains(text(), 'Change it later')]";
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.click();
                    return true;
                }
                return false;
            }""")
            if clicked:
                print("✅ Deep-Click SUCCESS.")
                await asyncio.sleep(2)
                await update_view(f"After Clicking Change It Later ({label})")
            else:
                print("ℹ️ Link not found on this screen.")

        try:
            # --- STEP 1: INITIAL LOAD ---
            await page.goto("https://apps.usw2.pure.cloud/directory/#", wait_until="networkidle")
            await update_view("1_Initial_Landing_Page")

            # --- STEP 2: MORE OPTIONS ---
            await page.get_by_text("More Login Options").click()
            await asyncio.sleep(2)
            await update_view("2_After_More_Options_Click")

            # --- STEP 3: SEARCH IHG ---
            await page.wait_for_selector("input[type='text']", state="visible")
            await page.fill("input[type='text']", "ihg")
            await update_view("3_Typed_IHG")
            await page.keyboard.press("Enter")
            await asyncio.sleep(3)
            await update_view("4_Search_Results_Loaded")

            # --- STEP 4: PING LOGO ---
            await page.wait_for_selector("img[alt='Ping Identity']", state="attached")
            await page.click("img[alt='Ping Identity']")
            await asyncio.sleep(5)
            await update_view("5_Redirected_to_Ping_SSO")

            # --- STEP 5: CREDENTIALS ---
            await page.wait_for_selector("input[name='pf.username']", state="visible")
            await page.fill("input[name='pf.username']", "UOARTG")
            await page.fill("input[name='pf.pass']", "Welc0metp@2027")
            await update_view("6_Credentials_Entered")
            
            # --- STEP 6: LOGIN CLICK ---
            print("🚀 Clicking Login...")
            await page.click("text=/Login/i")
            await asyncio.sleep(5)
            await update_view("7_Post_Login_Screen")

            # --- STEP 7: BYPASS ATTEMPT 1 ---
            await force_click_change_later("Pre-MFA")

            # --- STEP 8: MFA INTERACTION ---
            print("\n" + "!"*45)
            mfa_code = input("👉 ENTER YOUR 6-DIGIT PING AUTHENTICATOR CODE: ")
            print("!"*45 + "\n")

            await page.wait_for_selector("input", state="visible")
            await page.fill("input", mfa_code)
            await update_view("8_MFA_Code_Typed")
            
            await page.keyboard.press("Enter")
            print("⏳ MFA Submitted...")
            await asyncio.sleep(3)
            await update_view("9_After_MFA_Submit")

            # --- STEP 9: SUCCESS CHECK ---
            try:
                await page.wait_for_selector("text=Authenticated", timeout=15000)
                await update_view("10_MFA_AUTHENTICATED_GREEN_BOX")
            except:
                print("⚠️ 'Authenticated' text not detected visually.")

            # --- STEP 10: BYPASS ATTEMPT 2 ---
            await force_click_change_later("Post-MFA")

            # --- STEP 11: FINAL WAIT ---
            print("⏳ Final 15 second countdown starting...")
            for i in range(15, 0, -1):
                if i % 5 == 0: # Update view every 5 seconds during the wait
                    await update_view(f"Waiting_Redirection_{i}s_Left")
                await asyncio.sleep(1)

            # --- STEP 12: SAVE ---
            await page.wait_for_load_state("networkidle", timeout=60000)
            await update_view("11_FINAL_DASHBOARD")
            
            content = await page.content()
            with open("dashboard_source.html", "w", encoding="utf-8") as f:
                f.write(content)
            print("✅ DONE: Source saved to 'dashboard_source.html'")

        except Exception as e:
            print(f"❌ ERROR: {e}")
            await page.screenshot(path="error_state.png")
        finally:
            await browser.close()
            print("🏁 Session Closed.")

if __name__ == "__main__":
    asyncio.run(run())
