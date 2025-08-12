import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page_browser(context):
    page = context.new_page()
    yield page
    page.close()

def test_add_to_cart(page_browser: Page):
    page = page_browser
    # Login first
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    
    # Verify login was successful
    expect(page.locator("[data-test='title']")).to_be_visible()
    
    # Add item to cart
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")
    
    # Optional: Measure page load performance
    load_time = page.evaluate("performance.timing.loadEventEnd - performance.timing.navigationStart")
    print(f"Page load time: {load_time}ms")