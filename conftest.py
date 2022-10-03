import pytest
import allure
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        default="demo-opencart.com",
        help="Base application url"
    )
    parser.addoption(
        "--browser",
        default="chrome",
        help="Base browser for test"
    )


@pytest.fixture(scope="session")
def browser(request):
    base_url = request.config.getoption("--url")
    browser = request.config.getoption("--browser")

    capabilities = {
        "browserName": browser,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=capabilities)

    allure.attach(
        name="capabilities",
        body=str(driver.desired_capabilities),
        attachment_type=allure.attachment_type.TEXT
    )

    request.addfinalizer(driver.quit)

    driver.get(f"https://{base_url}")
    driver.base_url = f"https://{base_url}"

    return driver
