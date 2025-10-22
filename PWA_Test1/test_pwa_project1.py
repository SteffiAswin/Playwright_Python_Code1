from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest, csv, time
from PWA_Pages.pwa_feeds_poll_creation import pwa_feeds_poll_creation
from PWA_Pages.pwa_login_page import pwa_login_page
from PWA_Pages.pwa_feeds_post_creation import pwa_feeds_post_creation
from PWA_Pages.pwa_rewards import pwa_rewards
from PWA_Pages.pwa_frame_chat import pwa_frame_chat

def load_csv(path="/Users/apple/Desktop/Playwright_Python/Test_data/test_pwadata.csv"):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
    
# @pytest.mark.parametrize("data", load_csv())
# def test_pwa_first(data):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         loginPage = pwa_login_page(page)
#         loginPage.goto(data["url"])
#         loginPage.pwa_login(data["username"], data["password"])
#         page.wait_for_url("https://pwa.skordev.com/#/home")  
#         expect(page).to_have_url("https://pwa.skordev.com/#/home")
#         dashboard_header = page.get_by_text("Profile")
#         expect(dashboard_header).to_be_visible()
#         browser.close()
        
# @pytest.mark.parametrize("data", load_csv())
# def test_feeds_post_creation(data):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         loginPage = pwa_login_page(page)
#         loginPage.goto(data["url"])
#         loginPage.pwa_login(data["username"], data["password"])
#         page.wait_for_url("https://pwa.skordev.com/#/home")
#         feeds_actions = pwa_feeds_post_creation(page)
#         feeds_actions.click_feeds()
#         expect(page).to_have_url("https://pwa.skordev.com/#/feeds/appreciation")
        
#         feeds_actions.click_post_polls_and_plus()
#         expect(page.locator("mat-dialog-container")).to_be_visible()
        
#         post_title = data["post_title"]
#         post_content = data["post_content"]
#         feeds_actions.create_post(post_title, post_content)
        
#         expect(page.get_by_text(post_content)).to_be_visible(timeout=15000)
        
#         browser.close()
        
  
# @pytest.mark.parametrize("data", load_csv())
# def test_click_rewards(data):
#    with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         loginPage = pwa_login_page(page)
#         loginPage.goto(data["url"])
#         loginPage.pwa_login(data["username"], data["password"])
#         page.wait_for_url("https://pwa.skordev.com/#/home")
#         rewards_button = pwa_rewards(page)
#         rewards_button.click_rewards()
#         expect(page).to_have_url("https://pwa.skordev.com/#/rewards/browse-all")
#         browser.close()
        
# @pytest.mark.parametrize("data", load_csv())
# def test_search_and_redeem_reward(data):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         loginPage = pwa_login_page(page)
#         loginPage.goto(data["url"])
#         loginPage.pwa_login(data["username"], data["password"])
#         page.wait_for_url("https://pwa.skordev.com/#/home")
#         rewards_page = pwa_rewards(page)
#         rewards_page.click_rewards()
        
#         rewards_page.search_for_evoucher(data["reward_name"])
        
#         rewards_page.click_searched_evoucher(data["reward_name"]) 
#         if data["reward_name"] == "Dairy Farm $5 QA TESTING 2 then":
#             rewards_page.redeem_flow_3_steps_evoucher()
#         else:
#             rewards_page.redeem_flow_discount()

#         browser.close()
               
# @pytest.mark.parametrize("data", load_csv())
# def test_frame_chat_icon(data):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         loginPage = pwa_login_page(page)
#         loginPage.goto(data["url"])
#         loginPage.pwa_login(data["username"], data["password"])
#         page.wait_for_url("https://pwa.skordev.com/#/home")
#         chatbot = pwa_frame_chat(page)
#         chatbot.chatbot()
#         chatbot.type_query()
#         browser.close()

@pytest.mark.parametrize("data", load_csv())
def test_feeds_poll_creation(data, retries=3, delay=2):
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



















