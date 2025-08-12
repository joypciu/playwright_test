import pytest
from playwright.sync_api import Page, expect
from jira_integration import jira_issue, test_jira_connection
import os

# Set Jira credentials from environment variables
pytest.jira_username = os.getenv("JIRA_USERNAME")
pytest.jira_token = os.getenv("JIRA_TOKEN")

@pytest.fixture(scope="session", autouse=True)
def check_jira():
    """Check Jira connection before running any tests"""
    print("\n" + "🔍 SESSION SETUP: CHECKING JIRA CONNECTION" + "="*30)
    try:
        test_jira_connection()
        print("✅ JIRA CONNECTION: SUCCESS - Integration will be active")
    except Exception as e:
        print(f"⚠️  JIRA CONNECTION: ISSUES DETECTED")
        print(f"   Error: {e}")
        print("🔄 Tests will continue with limited Jira integration")
    print("="*70 + "\n")

@pytest.fixture(scope="function")
def page_browser(context):
    page = context.new_page()
    yield page
    page.close()

@jira_issue("KAN-2", "Test successful login flow")
def test_successful_login(page_browser: Page):
    print("🧪 EXECUTING: Successful Login Test")
    page = page_browser
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "standard_user")
    page.fill("[data-test='password']", "secret_sauce")
    page.click("[data-test='login-button']")
    expect(page.locator("[data-test='title']")).to_have_text("Products")
    page.screenshot(path="successful_login.png")
    print("✅ Login test completed successfully")

@jira_issue("KAN-3", "Test invalid login error handling")
def test_invalid_login(page_browser: Page):
    print("🧪 EXECUTING: Invalid Login Test")
    page = page_browser
    page.goto("https://www.saucedemo.com/")
    page.fill("[data-test='username']", "invalid_user")
    page.fill("[data-test='password']", "wrong_password")
    page.click("[data-test='login-button']")
    expect(page.locator("[data-test='error']").first).to_be_visible()
    page.screenshot(path="invalid_login_error.png")
    print("✅ Invalid login test completed successfully")

def test_jira_connection():
    """Standalone test for Jira connection"""
    print("🧪 EXECUTING: Jira Connection Test")
    from jira_integration import test_jira_connection
    test_jira_connection()
    print("✅ Jira connection test completed")