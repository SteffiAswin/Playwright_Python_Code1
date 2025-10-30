# PWA_Test1/test_login.py
# Final version for local + GitHub Actions use
# Compatible with Playwright Python, pytest, and your existing CSV structure

from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, os
from PWA_Pages.pwa_login_page import pwa_login_page


def load_csv(path="./Test_data/test_pwadata.csv"):
    """
    Loads login data from CSV file.
    Expected columns: url, username, password
    """
    try:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"❌ CSV file not found at {path}. Returning empty list.")
        return []


@pytest.mark.parametrize("data", load_csv())
def test_pwa_first(data):
    """
    Test: Launch PWA, perform login, verify navigation to home page.
    Captures network failures, video, and screenshots.
    """
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    print(f"🔹 Running in headless mode: {headless}")

    with sync_playwright() as p:
        # 📁 Directories for videos and screenshots
        video_dir = os.path.join(os.getcwd(), "videos")
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(video_dir, exist_ok=True)
        os.makedirs(screenshot_dir, exist_ok=True)

        # 🧱 Launch Chromium browser
        browser = p.chromium.launch(
            headless=headless,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        # 🌐 Browser context with video recording
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/100.0.4896.88 Safari/537.36"
            ),
            record_video_dir=video_dir,
        )

        # 🧭 Create new page
        page = context.new_page()

        # 🪝 Capture failed network requests for debugging
        failed_requests = []

        def log_failed_request(request):
            if request.failure:
                failed_requests.append(
                    f"❌ Failed request: {request.url} → {request.failure}"
                )

        page.on("requestfailed", log_failed_request)

        loginPage = pwa_login_page(page)
        expected_url = "https://pwa.skordev.com/#/home"

        try:
            print(f"🌍 Navigating to: {data['url']}")
            page.goto(data["url"], timeout=30000, wait_until="domcontentloaded")

            print(f"👤 Attempting login with username: {data['username']}")
            loginPage.pwa_login(data["username"], data["password"])

            print("⏳ Waiting for home page...")
            expect(page).to_have_url(expected_url, timeout=30000)

            print("✅ Login successful — Home page reached!")

        except TimeoutError:
            screenshot_path = os.path.join(screenshot_dir, "login_fail_FINAL_DEBUG.png")
            page.screenshot(path=screenshot_path)
            print(f"❌ Timeout: expected URL {expected_url}")
            print(f"📸 Screenshot saved to: {screenshot_path}")

            # Log failed network requests if any
            if failed_requests:
                print("\n🔍 Network request failures detected:")
                for fail in failed_requests:
                    print(fail)

            raise  # Re-raise for pytest to mark failure

        except Exception as e:
            screenshot_path = os.path.join(screenshot_dir, "login_unexpected_error.png")
            page.screenshot(path=screenshot_path)
            print(f"❌ Unexpected error: {e}")
            print(f"📸 Screenshot saved to: {screenshot_path}")
            raise

        finally:
            # 🧹 Cleanup: ensure video is available
            try:
                video_path = page.video.path() if page.video else None
            except Exception:
                video_path = None

            context.close()
            browser.close()

            if video_path and os.path.exists(video_path):
                print(f"🎥 Video recorded at: {video_path}")

            if failed_requests:
                print(f"⚠️ {len(failed_requests)} network requests failed.")
