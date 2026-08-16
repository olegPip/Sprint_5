import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators
from tests.helpers import generate_random_user_credentials
from tests.urls import TestUrls


class TestUserLogout:
    # Тесты лежат в отдельном классе и отдельном модуле

    def test_user_successful_logout(self, driver):
        # Тест успешного выхода из аккаунта пользователя
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Вызываем метод генерации уникальных данных напрямую из модуля helpers
        user_data = generate_random_user_credentials()
        unique_email = user_data["email"]
        password_value = user_data["password"]

        # Шаг 1. Регистрация нового пользователя для создания чистой авторизованной сессии
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(unique_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Проверяем успешность входа в систему по появлению аватара
        wait.until(EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))

        # Шаг 2. Выход из аккаунта (Logout)
        # Сначала кликаем по аватару пользователя через JavaScript для надежности в React UI
        profile_btn = wait.until(EC.element_to_be_clickable(RegistrationLocators.USER_AVATAR))
        driver.execute_script("arguments[0].click();", profile_btn)

        # Кликаем по появившейся кнопке «Выйти»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGOUT_BUTTON)).click()

        # Шаг 3. Проверка фактического результата
        # Кнопка «Вход и регистрация» должна вернуться в шапку сайта
        is_login_button_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.LOGIN_REG_BUTTON)
        ).is_displayed()

        # Аватар пользователя должен скрыться из DOM-дерева
        is_avatar_hidden = wait.until(
            EC.invisibility_of_element_located(RegistrationLocators.USER_AVATAR)
        )

        # Финальные однозначные ассерты согласно требованиям вашего проекта
        assert is_login_button_visible is True, "Кнопка входа не появилась после логаута"
        assert is_avatar_hidden is True, "Аватар пользователя остался видимым после логаута"
