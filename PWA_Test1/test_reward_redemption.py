from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time

from PWA_Pages.pwa_login_page import pwa_login_page
from PWA_Pages.pwa_rewards import pwa_rewards



def load_csv(path="/Users/apple/Desktop/Playwright_Python/Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

@pytest.mark.parametrize("data", load_csv())
def test_search_and_redeem_reward(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        loginPage = pwa_login_page(page)
        loginPage.goto(data["url"])
        loginPage.pwa_login(data["username"], data["password"])
        page.wait_for_url("https://pwa.skordev.com/#/home")
        rewards_page = pwa_rewards(page)
        rewards_page.click_rewards()
        
        rewards_page.search_for_evoucher(data["reward_name"])
        
        rewards_page.click_searched_evoucher(data["reward_name"]) 
        if data["reward_name"] == "Dairy Farm $5 QA TESTING 2":
            rewards_page.redeem_flow_3_steps_evoucher()
        else:
            rewards_page.redeem_flow_discount()

        browser.close()