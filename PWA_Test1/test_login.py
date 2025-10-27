# PWA_Test1/test_login.py (Final Version)

from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, os 

from PWA_Pages.pwa_login_page import pwa_login_page


def load_csv(path="./Test_data/test_pwadata.csv"):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {path}. Returning empty list.")
        return []

    
@pytest.mark.parametrize("data", load_csv())
def test_pwa_first(data):
    # Set headless=True (where the test needs to succeed)
    with sync_playwright() as p:
        
        # FIX: Added launch arguments to stabilize and mask the headless browser
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox'] 
        )
        
        # FIX: Added User Agent and Viewport to mimic a standard desktop session
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
        )
        page = context.new_page()
        
        loginPage = pwa_login_page(page)
        
        # 1. Navigate to the login page
        page.goto(data["url"])
        
        # 2. Perform the login action
        loginPage.pwa_login(data["username"], data["password"])
        
        # 3. Wait for navigation until 'networkidle' state
        expected_url = "https://pwa.skordev.com/#/home"

        try:
            # page.wait_for_url(expected_url, wait_until="networkidle", timeout=20000)
            current_url = page.url
            print("Current page URL:", current_url)
            # If the wait passes, assert success
            expect(page).to_have_url(expected_url)
            print("Test passed in headless mode! 🎉")

        except TimeoutError:
            # Re-raise the error after taking a final screenshot for diagnosis
            screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login_fail_FINAL_DEBUG.png")
            page.screenshot(path=screenshot_path)
            print(f"\n!!! FAIL: Timeout on {expected_url}. Screenshot saved to {screenshot_path}.")
            
            # If the test still fails, the problem is bad test data (invalid credentials) 
            # or a very aggressive security check blocking all automated browsers.
            raise
        
        browser.close()
