# PWA_Test1/test_login.py (Final Version with Video & Safe Teardown)

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
    # Allow headless toggle via environment variable
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    print(f"Running in headless mode: {headless}")

    with sync_playwright() as p:
        # Record videos for all sessions
        video_dir = os.path.join(os.getcwd(), "videos")
        os.makedirs(video_dir, exist_ok=True)

        # Launch with hardened args
        browser = p.chromium.launch(
            headless=headless,
            args=["--disable-gpu", "--no-sandbox", "--disable-setuid-sandbox"]
        )

        # Create context with video recording enabled
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/100.0.4896.88 Safari/537.36"
            ),
            record_video_dir=video_dir,  
        )

        page = context.new_page()
        loginPage = pwa_login_page(page)

        expected_url = "https://pwa.skordev.com/#/home"

        try:
            # Navigate to login page
            page.goto(data["url"])

            # Perform login
            loginPage.pwa_login(data["username"], data["password"])

            # Wait and verify navigation
            expect(page).to_have_url(expected_url, timeout=20000)
            print("Test passed in headless mode!")

        except TimeoutError:
            # Capture failure evidence
            screenshot_path = os.path.join(os.getcwd(), "screenshots", "login_fail_FINAL_DEBUG.png")
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"Timeout: expected {expected_url}. Screenshot saved to {screenshot_path}")
            raise

        finally:
            # Wait for video file to be fully written
            video_path = page.video.path() if page.video else None
            context.close()
            browser.close()

            # Move or log video file for artifact upload
            if video_path:
                print(f"Video recorded at: {video_path}")
