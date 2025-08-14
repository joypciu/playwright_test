import pytest

@pytest.fixture(scope="function")
def page_browser(page):
    yield page
    page.close()
