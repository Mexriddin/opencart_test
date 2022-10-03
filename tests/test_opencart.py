import allure
import pytest
import faker
import selenium
from selenium.webdriver.common.by import By


@pytest.mark.authorization
@allure.feature("Авторизвция")
@allure.title("Проверка валидный авторизации")
def test_authorization_valid(browser):
    login = "demo"
    password = "demo"
    with allure.step("Переход в раздел администратора"):
        browser.get(f"{browser.base_url}/admin/")

    with allure.step(f"Ввести логин: {login}"):
        browser.find_element(By.CSS_SELECTOR, "#input-username").send_keys(login)

    with allure.step(f"Ввести пароль: {password}"):
        browser.find_element(By.CSS_SELECTOR, "#input-password").send_keys(password)

    with allure.step("Нажать на кнопку 'Войти'"):
        browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary").submit()

    with allure.step("Проверка отображение админки"):
        try:
            browser.find_element(By.CSS_SELECTOR, "#user-profile").click()
            browser.find_element(By.CSS_SELECTOR, "#afga")
        except selenium.common.exceptions.NoSuchElementException as e:
            allure.attach(
                name="error_screenshot",
                body=browser.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(e)



@allure.feature("Общие проверки")
@allure.title("Проверка тайтла главный страницы")
def test_example(browser):
    with allure.step("Переход в раздел администратора"):
        browser.get(f"{browser.base_url}")

    with allure.step("Проверка тайтл страницы"):
        assert browser.title == "Your Store"
