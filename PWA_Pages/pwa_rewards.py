from playwright.sync_api import Page, expect

class pwa_rewards:
    def __init__(self, page: Page):
        self.page = page
        self.rewards_button = page.locator("[class='icon icon-rewards']").nth(1)
        self.search_bar = page.locator("[class='form-control form-control-lg input--search ng-untouched ng-pristine ng-valid']")
        self.evoucher_reward = lambda reward_name: self.page.get_by_role("heading", name=reward_name)
        self.redeem_button_main_evoucher = page.get_by_role("button", name="Redeem")
        self.redeem_now_button_detail_evoucher = page.get_by_text("Redeem Now")
        self.redeem_now_button_popup_evoucher = page.get_by_text("Redeem Now").nth(2)
        self.redemption_success_message_evoucher = page.get_by_text("Redemption Successful")
        self.search_results_evoucher = self.page.get_by_text("result found")
        self.redeem_button_main_discount = self.page.get_by_role("button", name="Redeem")
        self.redemption_success_message_discount = self.page.get_by_role("heading")
        
    def click_rewards(self):
        self.rewards_button.click()
        self.page.wait_for_url("https://pwa.skordev.com/#/rewards/browse-all")
        
    def search_for_evoucher(self, reward_name: str):
        self.search_bar.fill(reward_name) 
        self.search_results_evoucher.wait_for()
        
    def click_searched_evoucher(self, reward_name: str):
        self.evoucher_reward(reward_name).click()
        self.page.wait_for_url("https://pwa.skordev.com/#/reward/*")
        
     
    def redeem_flow_3_steps_evoucher(self):
        self.redeem_button_main_evoucher.click()
        self.redeem_now_button_detail_evoucher.click()
        self.page.wait_for_selector("text=Redeem Confirmation")
        self.redeem_now_button_popup_evoucher.click()
        self.redemption_success_message_evoucher.wait_for()
        
    def redeem_flow_discount(self):
        self.redeem_button_main_discount.click()
        expect(self.redemption_success_message_discount).to_contain_text("Reward Redeemed!")
        self.page.pause()
        
            