import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators


class TestUserRegistration:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_registration_already_existing_user_shows_errors(self, driver):
        # Тест регистрации уже существующего пользователя.
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Генерируем новый Email для регистрации
        existing_email = f"existing_user_{int(time.monotonic())}@test.ru"
        password_value = "TestPassword123"

        # ШАГ 1: СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ, КОТОРЫЙ СТАНЕТ «СУЩЕСТВУЮЩИМ»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(existing_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Ждем успешного входа, чтобы убедиться, что пользователь создался в БД
        wait.until(EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))

        # Разлогиниваемся, чтобы вернуться в исходное состояние
        wait.until(EC.element_to_be_clickable(RegistrationLocators.USER_AVATAR)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGOUT_BUTTON)).click()

        # ШАГ 2: ПЫТАЕМСЯ ЗАРЕГИСТРИРОВАТЬ ЕГО ЖЕ ПОВТОРНО
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        # Заполняем форму теми же самыми данными
        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(existing_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # ШАГ 3: ПРОВЕРКА ОШИБОК И АССЕРТЫ
        email_error = wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_ERROR_CONTAINER))
        password_error = driver.find_element(*RegistrationLocators.PASSWORD_ERROR_CONTAINER)
        confirm_password_error = driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_ERROR_CONTAINER)
        error_message_element = driver.find_element(*RegistrationLocators.EMAIL_ERROR_MESSAGE)

        # Вытаскиваем фактические данные
        is_email_red = email_error.is_displayed()
        is_password_red = password_error.is_displayed()
        is_confirm_red = confirm_password_error.is_displayed()
        actual_error_text = error_message_element.text
        expected_error_text = "Ошибка"

        # Финальные ассерты со сравнением фактического и ожидаемого результатов
        assert is_email_red is True, "Поле Email не подсветилось красным при повторной регистрации"
        assert is_password_red is True, "Поле Пароль не подсветилось красным при повторной регистрации"
        assert is_confirm_red is True, "Поле Подтверждение пароля не подсветилось красным"

        assert actual_error_text == expected_error_text, (
            f"Неверный текст ошибки. Ожидалось: '{expected_error_text}', получено: '{actual_error_text}'")
