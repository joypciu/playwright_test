import pytest
from playwright.sync_api import Page, expect
from jira_integration import jira_issue
import os

# Set Jira credentials from environment variables
pytest.jira_username = os.getenv("JIRA_USERNAME")
pytest.jira_token = os.getenv("JIRA_TOKEN")

@jira_issue("KAN-1", "Test the complete checkout flow")
def test_checkout(page_browser: Page):
    page = page_browser

    # Login first
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    
    # Verify login was successful
    expect(page.locator("[data-test='title']")).to_be_visible()
    expect(page.locator("[data-test='title']")).to_have_text("Products")

    # Add items to cart
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
    page.click("[data-test='shopping-cart-link']")
    page.screenshot(path="cart.png")

    # Remove an item from the cart
    page.click("[data-test='remove-sauce-labs-backpack']")

    # Proceed to checkout
    page.click("[data-test='checkout']")
    expect(page.locator("[data-test='firstName']")).to_be_visible()
    
    # Fill in checkout information
    page.fill("[data-test='firstName']", "u")
    page.fill("[data-test='lastName']", "j")
    page.fill("[data-test='postalCode']", "123")
    page.click("[data-test='continue']")
    expect(page.locator("[data-test='finish']")).to_be_visible()
    
    # Finish the checkout process
    page.click("[data-test='finish']")
    expect(page.locator("[data-test='back-to-products']")).to_be_visible()
    page.screenshot(path="checkout_complete.png")