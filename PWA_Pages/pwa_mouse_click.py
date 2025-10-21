from playwright.sync_api import Page, Expect
class pwa_mouse_click:
    def __init__(self,page:Page):
        self.page= page
    
    def mouse_click(self):
        