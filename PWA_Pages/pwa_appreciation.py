import time
from playwright.sync_api import Page, expect

class Pwa_Appreciation:
    def __init__(self, page: Page):
        self.page = page
        self.thanks_button = page.locator("mat-drawer-content app-left-navigate").get_by_text("Thanks")
        self.OntheSpot_button = page.get_by_text("On the Spot Send a quick")
        self.search_appreciation_receiver_button = page.get_by_role("searchbox", name="Search")
        self.receiver = page.get_by_role("heading", name="Charles Kieth")
        self.select_core_value = page.locator("app-core-value div").filter(has_text="Consistency").nth(1)
        
        
        

    def click_thanks(self):
     self.thanks_button.click()
     
    def click_OntheSpot(self):
        self.OntheSpot_button.click()
    
    def search_and_selectUser(self, appreciation_receiver_email: str, expected_user_name: str = 'Charles Kieth'):
        self.search_appreciation_receiver_button.fill(appreciation_receiver_email)
        self.receiver.click()
        
    def on_the_spot(self):
        self.select_core_value.click() 
        
            
         
    