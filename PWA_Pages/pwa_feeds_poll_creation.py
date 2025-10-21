import time
from playwright.sync_api import Page, expect

class pwa_feeds_poll_creation:
    def __init__(self, page: Page):
        self.page = page
        self.feeds_button = page.locator("mat-drawer-content app-left-navigate").get_by_text("Feeds")
        self.post_polls_button = page.get_by_text('Post & Polls')
        self.plus_icon = page.locator("app-float-add-btn div").nth(1)
        self.select_poll_button = page.get_by_text("Poll", exact=True)
        # Corrected locator for the poll question input field based on placeholder
        self.poll_question_input = page.get_by_placeholder("Write Your Question")
        
        # Consistent locator for the single, always-visible option input field
        self.poll_option_input = page.locator('input[placeholder="+ Add Option"]')
        
        self.post_to_organization = page.locator("app-add-poll").get_by_text('Organization')
        
        self.create_button = page.get_by_role("button", name="Create")

    def create_poll(self, question: str, options: list[str]):
        # Navigate to the poll creation form
        self.feeds_button.click()
        self.post_polls_button.click()
        self.plus_icon.click()
        self.select_poll_button.click()
        
        # Explicitly wait for the poll creation form to be visible.
        expect(self.page.get_by_text('Create Poll')).to_be_visible()
        
        # First, fill the poll question.
        self.poll_question_input.fill(question)
        
        # Then, fill all provided options dynamically.
        for option_text in options:
            # Always locate the single, available option input field
            self.poll_option_input.fill(option_text)
            
            # Press 'Enter' to confirm the option and create the next one
            self.page.keyboard.press("Enter")
            
        # Select 'Post to Organization'
        self.post_to_organization.click()
        
        # Wait for the create button to become enabled after filling all options.
        expect(self.create_button).to_be_enabled()
        
        # Click the Create button
        self.create_button.click()
        
        # Wait for the modal to close by waiting for the create button to become hidden.
        expect(self.create_button).to_be_hidden()