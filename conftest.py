import pytest
import os

def pytest_configure(config):
    """Configure pytest-html to generate reports automatically"""
    if not config.option.htmlpath:
        config.option.htmlpath = "report.html"
    if not config.option.self_contained_html:
        config.option.self_contained_html = True

@pytest.fixture(scope="function")
def page_browser(page):
    yield page
    page.close()
