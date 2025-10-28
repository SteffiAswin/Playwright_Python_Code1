import os
import pytest
from playwright.sync_api import sync_playwright, expect

@pytest.mark.saucedemo
def test_saucedemo_add_to_cart():
    headless = os.getenv("HEADLESS", "True").lower() == "true"
    print(f"Running in headless mode: {headless}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, slow_mo=200)
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()

        try:
            # 1️⃣ Navigate to SauceDemo
            page.goto("https://www.saucedemo.com/")

            # 2️⃣ Login
            page.fill("#user-name", "standard_user")
            page.fill("#password", "secret_sauce")
            page.click("#login-button")

            # 3️⃣ Verify login success
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
            print("✅ Login successful!")

            # 4️⃣ Add first two products to cart
            page.click('button[id="add-to-cart-sauce-labs-backpack"]')
            page.click('button[id="add-to-cart-sauce-labs-bike-light"]')
            print("🛒 Added Backpack and Bike Light to cart")

            # 5️⃣ Verify cart badge count
            cart_badge = page.locator(".shopping_cart_badge")
            expect(cart_badge).to_have_text("2")

            # 6️⃣ Click cart and verify items
            page.click(".shopping_cart_link")
            expect(page).to_have_url("https://www.saucedemo.com/cart.html")

            # Verify both items are in the cart
            expect(page.locator(".cart_item")).to_have_count(2)
            print("✅ Cart contains 2 items")

        except Exception as e:
            # Screenshot on failure
            screenshot_path = "screenshots/add_to_cart_failure.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            page.screenshot(path=screenshot_path)
            print(f"❌ Test failed. Screenshot saved at: {screenshot_path}")
            raise e

        finally:
            context.close()
            browser.close()
