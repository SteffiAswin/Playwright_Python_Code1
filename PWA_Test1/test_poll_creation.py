from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time

from PWA_Pages.pwa_feeds_poll_creation import pwa_feeds_poll_creation
from PWA_Pages.pwa_login_page import pwa_login_page



def load_csv(path="/Users/apple/Desktop/Playwright_Python/Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


@pytest.mark.parametrize("data", load_csv())
def test_feeds_poll_creation(data, retries=1, delay=2):
    for attempt in range(retries):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
            
                loginPage = pwa_login_page(page)
                loginPage.goto(data["url"])
                loginPage.pwa_login(data["username"], data["password"])
                
                page.wait_for_url("https://pwa.skordev.com/#/home")
                
                poll_creator = pwa_feeds_poll_creation(page)
                options_list = data["poll_options"].split(',')
                
                # This method creates the poll and leaves the user on the post-n-polls page.
                poll_creator.create_poll(data["poll_question"], options_list)
                
                # Now, explicitly navigate to the correct URL where the poll is visible.
                page.goto("https://pwa.skordev.com/#/feeds/post-n-polls")
                page.pause()
                # Wait for the poll's container to appear on the page.
                poll_container_locator = page.locator("app-item")
                
                poll_locator = poll_container_locator.get_by_text(data["dummy_question"], exact=True).nth(-1)
                print(poll_locator)
                expect(poll_locator).to_be_visible(timeout=2000)
                
                browser.close()

                break
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt==2:
                raise
            time.sleep(delay)