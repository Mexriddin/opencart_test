import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ch_s
from selenium.webdriver.firefox.service import Service as fr_s
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption("--url", default="demo-opencart.com", help="Base application url")
    parser.addoption("--browser", default="chrome", help="Base browser for test")
    parser.addoption("--brversion", default="105", help="Default version browser")
    parser.addoption("--executor", default="local", help="Executor for running test")
    parser.addoption("--vnc", action="store_true", default=True)
    parser.addoption("--video", action="store_true", default=True)


def driver_factory(browser, brversion, executor, vnc, video):
    if executor == "local":
        if browser == "chrome":
            service = ch_s(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
        elif browser == "firefox":
            service = fr_s(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)
        else:
            raise Exception("Browser not supported")
    else:
        executor_url = f"http://{executor}:4444/wd/hub"
        caps = {
            "browserName": browser,
            "browserVersion": brversion,
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": video
            }
        }
        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps
        )
    driver.maximize_window()
    return driver


@pytest.fixture(scope="session")
def browser(request):
    base_url = request.config.getoption("--url")
    browser = request.config.getoption("--browser")
    brversion = request.config.getoption("--brversion")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    video = request.config.getoption("--video")

    driver = driver_factory(browser=browser, brversion=brversion,
                            executor=executor, vnc=vnc, video=video)

    allure.attach(
        name="capabilities",
        body=str(driver.desired_capabilities),
        attachment_type=allure.attachment_type.TEXT
    )

    request.addfinalizer(driver.quit)

    driver.get(f"https://{base_url}")
    driver.base_url = f"https://{base_url}"

    return driver
