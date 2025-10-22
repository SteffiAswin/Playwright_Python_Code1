from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time
import base64

from PWA_Pages.pwa_login_page import pwa_login_page


def load_csv(path="./Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
@pytest.mark.parametrize("data", load_csv())
def test_pwa_first(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.wait_for_timeout(3000);
        page.set_default_timeout(600000)
        loginPage = pwa_login_page(page)
        loginPage.goto(data["url"])
        print(data["username"])
        print(data["password"])
        loginPage.pwa_login(data["username"], data["password"])
        screenshot_bytes = page.screenshot(full_page=True)
        screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
        print("SCREENSHOT_BASE64_START")
        print(screenshot_base64)
        print("SCREENSHOT_BASE64_END")
        current_url = page.url
        print("Current page URL:", current_url)
        # page.wait_for_url("https://pwa.skordev.com/#/home")  
        # expect(page).to_have_url("https://pwa.skordev.com/#/home")
        # dashboard_header = page.get_by_text("Profile")
        # expect(dashboard_header).to_be_visible()
        browser.close()
        
        # 
