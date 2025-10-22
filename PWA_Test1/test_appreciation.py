from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time

from PWA_Pages.pwa_appreciation import Pwa_Appreciation
from PWA_Pages.pwa_login_page import pwa_login_page



def load_csv(path="/Users/apple/Desktop/Playwright_Python/Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
@pytest.mark.parametrize("data", load_csv())
def test_appreciation(data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        loginPage = pwa_login_page(page)
        loginPage.goto(data["url"])
        loginPage.pwa_login(data["username"], data["password"])
        page.wait_for_url("https://pwa.skordev.com/#/home")
        thanks_actions = Pwa_Appreciation(page)
        thanks_actions.click_thanks()
        expect(page).to_have_url("https://pwa.skordev.com/#/appreciate/mode")
        
        thanks_actions.click_OntheSpot()
        expect(page).to_have_url("https://pwa.skordev.com/#/appreciate/user")
        
        thanks_actions.search_and_selectUser(appreciation_receiver_email=data["appreciation_receiver_email"])
        expect(page).to_have_url("https://pwa.skordev.com/#/appreciate/do")
        
        thanks_actions.on_the_spot()
        # testing git
        