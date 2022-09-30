import pytest
from selenium import webdriver


@pytest.fixture()
def browser(request):
    capabilities = {
        "browserName": "chrome",
        "browserVersion": "105.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=capabilities)

    request.addfinalizer(driver.quit())
    return driver



