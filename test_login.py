import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page_browser(context):
    page = context.new_page()
    yield page
    page.close()

def test_successful_login(page_browser: Page):
    page = page_browser
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    expect(page.locator("[data-test='title']")).to_have_text("Products")
    page.screenshot(path="successful_login.png")  # For debugging

def test_invalid_login(page_browser: Page):
    page = page_browser
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "invalid_user")
    page.fill("[data-test='password']", "wrong_password")
    page.click("[data-test='login-button']")
    expect(page.locator("[data-test='error']")).to_be_visible()
    page.screenshot(path="invalid_login_error.png")  # For debugging