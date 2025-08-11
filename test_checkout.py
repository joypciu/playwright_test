import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="function")
def page_browser(context):
    page = context.new_page()
    yield page
    page.close()

def test_checkout(page_browser: Page):
    page = page_browser

    #login first
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    if not page.is_visible("[data-test='title']"):
        raise Exception("Login failed, title not visible")
    
    expect(page.locator("[data-test='title']")).to_be_visible()

    # Add items to cart
    page.click("[data-test='add-to-cart-sauce-labs-backpack']")
    page.click("[data-test='add-to-cart-sauce-labs-bike-light']")
    page.click("[data-test='shopping-cart-link']")
    page.screenshot(path="cart.png")

    ## Remove an item from the cart
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




# test('test', async ({ page }) => {
#   await page.goto('https://www.saucedemo.com/');
#   await page.locator('[data-test="username"]').click();
#   await page.locator('[data-test="username"]').fill('standard_user');
#   await page.locator('[data-test="password"]').click();
#   await page.locator('[data-test="password"]').fill('secret_sauce');
#   await page.locator('[data-test="login-button"]').click();
#   await page.locator('[data-test="title"]').click();
#   await page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click();
#   await page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click();
#   await page.locator('[data-test="shopping-cart-link"]').click();
#   await page.locator('[data-test="remove-sauce-labs-backpack"]').click();
#   await page.locator('[data-test="checkout"]').click();
#   await page.locator('[data-test="firstName"]').click();
#   await page.locator('[data-test="firstName"]').fill('u');
#   await page.locator('[data-test="lastName"]').click();
#   await page.locator('[data-test="lastName"]').fill('j');
#   await page.locator('[data-test="postalCode"]').click();
#   await page.locator('[data-test="postalCode"]').fill('123');
#   await page.locator('[data-test="continue"]').click();
#   await page.locator('[data-test="finish"]').click();
#   await page.locator('[data-test="back-to-products"]').click();
# });