from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, os, time
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
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            slow_mo=250,
            args=['--disable-gpu', '--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', { get: () => undefined })")

        loginPage = pwa_login_page(page)

        print(f"\nNavigating to {data['url']} ...")
        page.goto(data["url"], wait_until="networkidle")

        loginPage.pwa_login(data["username"], data["password"])
        time.sleep(2)  # allow redirect

        expected_url = "https://pwa.skordev.com/#/home"
        try:
            page.wait_for_url(expected_url, timeout=20000)
            expect(page).to_have_url(expected_url)
            print("Test passed in headless mode!")

        except TimeoutError:
            screenshot_path = os.path.join(os.path.dirname(__file__), "login_fail_FINAL_DEBUG.png")
            page.screenshot(path=screenshot_path)
            print(f"Timeout on {expected_url}. Screenshot: {screenshot_path}")
            raise

        browser.close()
