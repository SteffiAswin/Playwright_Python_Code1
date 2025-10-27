# PWA_Pages/pwa_login_page.py

from playwright.sync_api import Page, Expect, expect
class pwa_login_page:
    def __init__(self,page:Page):
        self.page = page
        
        # FIX: Use generic locators to find the input fields reliably
        # Assuming the first text/email input is the username field
        self.username = page.locator('input[type="text"], input[type="email"]').first
        self.password = page.locator("input[type=\"password\"]")
        
        # FIX: Use the most robust button locator
        self.loginbutton = page.get_by_role("button", name="Login") 
        
    def pwa_login(self,username:str,password:str):
        
        # FIX: Explicitly wait for the username field to be visible before filling
        self.username.wait_for(state="visible", timeout=10000)
        
        self.username.fill(username)  
        self.password.fill(password)
        
        # FIX: Use expect to wait for the button to be enabled before clicking
        expect(self.loginbutton).to_be_enabled(timeout=5000)
        self.loginbutton.click()