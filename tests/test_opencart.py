import time
from selenium.webdriver.common.by import By


def test_authorization_valid(browser):

    browser.get("https://demo-opencart.com/admin/")

    # Ввести логин
    browser.find_element(By.CSS_SELECTOR, "#input-username").send_keys("demo")

    # Ввести пароль
    browser.find_element(By.CSS_SELECTOR, "#input-password").send_keys("demo")

    #Подтвердить вход
    browser.find_element(By.CSS_SELECTOR, ".btn.btn-primary").submit()

    # Проверить что авторизация прошла успешно
    browser.find_element(By.CSS_SELECTOR, "#user-profile").click()

