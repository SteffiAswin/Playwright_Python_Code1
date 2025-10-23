from playwright.sync_api import Page, Expect, expect
class pwa_login_page:
    def __init__(self,page:Page):
        self.page= page
        # self.username= page.locator("[name='loginId']")
        # self.password= page.locator("[formcontrolname='password']")
        self.username=page.locator("#loginId")
        self.password=page.locator("[type='password']")
        self.loginbutton= page.get_by_role("button", name="Login")
        
    def pwa_login(self,username:str,password:str):
        self.username.fill(username)  
        self.password.fill(password)
        # cordinates= self.loginbutton.bounding_box()
        # print(cordinates)
        self.page.wait_for_timeout(3000)
        expect(self.page.locator("#loginId")).to_have_value(username);
        expect(self.page.locator("input[type=\"password\"]")).to_have_value(password)
        self.loginbutton.click()
        self.page.wait_for_timeout(3000)
        
    def goto(self,url:str):
        self.page.goto(url)    
        
      
        
