import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.saucedemo
def test_saucedemo_login():
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    print(f"Running in headless mode: {headless}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=200)
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()

        try:
            # Navigate to SauceDemo
            page.goto("https://www.saucedemo.com/")

            # Perform login
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")

            # Assert successful login
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
            print("✅ Login successful!")

        except Exception as e:
            # Take a screenshot if the test fails
            screenshot_path = "screenshots/login_failure.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"❌ Test failed. Screenshot saved at: {screenshot_path}")
            raise e

        finally:
            context.close()
            browser.close()
