import pytest
from selene import browser

@pytest.fixture(scope="function", autouse=True)
def browser_manage():
    browser.config.base_url = 'https://demoqa.com/automation-practice-form'
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield
    browser.quit()

@pytest.fixture()
def js_commands():
    browser.config.type_by_js = True
    browser.config.click_by_js = True
