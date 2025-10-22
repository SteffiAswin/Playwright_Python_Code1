from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time

from PWA_Pages.pwa_login_page import pwa_login_page
from PWA_Pages.pwa_feeds_post_creation import pwa_feeds_post_creation


def load_csv(path="/Users/apple/Desktop/Playwright_Python/Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
@pytest.mark.parametrize("data", load_csv())
def test_feeds_post_creation(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        loginPage = pwa_login_page(page)
        loginPage.goto(data["url"])
        loginPage.pwa_login(data["username"], data["password"])
        page.wait_for_url("https://pwa.skordev.com/#/home")
        feeds_actions = pwa_feeds_post_creation(page)
        feeds_actions.click_feeds()
        expect(page).to_have_url("https://pwa.skordev.com/#/feeds/appreciation")
        
        feeds_actions.click_post_polls_and_plus()
        expect(page.locator("mat-dialog-container")).to_be_visible()
        
        post_title = data["post_title"]
        post_content = data["post_content"]
        feeds_actions.create_post(post_title, post_content)
        
        expect(page.get_by_text(post_content)).to_be_visible(timeout=15000)
        
        browser.close()