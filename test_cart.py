import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page_browser(context):
    page = context.new_page()
    yield page
    page.close()

def test_add_to_cart(page_browser: Page):
    page = page_browser
    # Login first (reuse code or make a fixture)
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("1")

    page.evaluate("performance.timing.loadEventEnd - performance.timing.navigationStart")