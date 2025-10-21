from playwright.sync_api import Page

class pwa_feeds_post_creation:
    def __init__(self, page: Page):
        self.page = page
        self.feeds_button = page.locator("mat-drawer-content app-left-navigate").get_by_text("Feeds")
        self.post_polls_button = page.get_by_text('Post & Polls')
        self.plus_icon = page.locator("app-float-add-btn div").nth(1)
        self.title_input = page.get_by_role("textbox", name="Title")
        self.post_textarea = page.get_by_role("textbox", name="What would you like to post?")
        self.organization_button = page.locator("app-add-post").get_by_text("Organization")
        self.post_button = page.get_by_role("button", name="Post")
    
    def click_feeds(self):
        self.feeds_button.click()
        
    def click_post_polls_and_plus(self):
        self.post_polls_button.click()
        self.plus_icon.click()
        
    def create_post(self, title: str, content: str):    
        self.title_input.fill(title)   
        self.post_textarea.fill(content)
        self.organization_button.click()
        self.post_button.click() 
        
        
