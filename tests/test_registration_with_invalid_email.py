import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators


class TestUserRegistration:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_registration_with_invalid_email_format_shows_errors(self, driver):
        # Тест регистрации с email не по маске *******@*******.***
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Email для тестов регистрации генерируется каждый раз новый.
        # Генерируем некорректный формат (например: invalid_17182103@test.r — не хватает символов в домене)
        invalid_unique_email = f"invalid_{int(time.monotonic())}@test.r"
        valid_password = "TestPassword123"

        # Шаг 1. Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()

        # Шаг 2. Нажать кнопку «Нет аккаунта»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        # Шаг 3. Заполнить поле Email не по маске, а также поля паролей
        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(invalid_unique_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(valid_password)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(valid_password)

        # Нажать кнопку «Создать аккаунт»
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Шаг 4. Получение элементов ошибок (с фиксацией фактических состояний)
        email_error = wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_ERROR_CONTAINER))
        password_error = driver.find_element(*RegistrationLocators.PASSWORD_ERROR_CONTAINER)
        confirm_password_error = driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_ERROR_CONTAINER)
        error_message_element = driver.find_element(*RegistrationLocators.EMAIL_ERROR_MESSAGE)

        # Сбор данных для финальных проверок
        is_email_red = email_error.is_displayed()
        is_password_red = password_error.is_displayed()
        is_confirm_red = confirm_password_error.is_displayed()

        actual_error_text = error_message_element.text
        expected_error_text = "Ошибка"

        # Финальные ассерты со сравнением фактического и ожидаемого результатов
        assert is_email_red is True, "Поле Email не выделилось красным цветом при ошибке"
        assert is_password_red is True, "Поле Пароль не выделилось красным цветом при ошибке"
        assert is_confirm_red is True, "Поле Подтверждение пароля не выделилось красным цветом при ошибке"

        assert actual_error_text == expected_error_text, (
            f"Неверный текст ошибки под полем Email. "
            f"Ожидалось: '{expected_error_text}', но получено: '{actual_error_text}'")