from playwright.sync_api import Page, Expect
class pwa_frame_chat:
    def __init__(self,page:Page):
        self.page= page
    
    def chatbot(self):
        self.page.wait_for_timeout(5000)
        frame = self.page.frame(name="fc_widget")
        chat_icon = frame.locator("[id='chat-icon']")
        chat_icon.click()
        
        
    def type_query(self):    
        frame = self.page.frame(name="fc_widget")
        frame.locator("[aria-label='Your email']").fill("playwright1@gmail.com")
        self.page.pause()
        