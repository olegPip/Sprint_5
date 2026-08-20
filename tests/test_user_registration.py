import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators
from helpers import generate_random_user_credentials
from tests.urls import TestUrls


class TestUserRegistration:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_user_registration_flow(self, driver):
        # Тест успешной регистрации нового пользователя.
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Вызываем метод генерации данных напрямую из модуля helpers
        user_data = generate_random_user_credentials()
        unique_email = f"test_{int(time.time())}@test.ru"
        password_value = "ValidPassword123!"

        # Шаг 1. Нажать кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()

        # Шаг 2. Нажать кнопку «Нет аккаунта»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        # Шаг 3. Заполнить все поля формы регистрации уникальными данными
        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(unique_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)

        # Нажать кнопку «Создать аккаунт»
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Шаг 4. Получение элементов для проверки фактического результата
        is_add_ad_btn_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.ADD_AD_BUTTON)
        ).is_displayed()

        user_avatar_element = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))
        is_avatar_visible = user_avatar_element.is_displayed()

        user_name_element = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_NAME_HEADER))
        is_name_visible = user_name_element.is_displayed()
        actual_user_name_text = user_name_element.text
        expected_name_part = "User"

        # Финальные ассерты со сравнением фактического и ожидаемого результатов
        assert is_add_ad_btn_visible is True, "Кнопка размещения объявления не появилась после регистрации"
        assert is_avatar_visible is True, "Аватар пользователя не отображается в шапке сайта"
        assert is_name_visible is True, "Имя пользователя отсутствует на странице профиля"

        assert expected_name_part in actual_user_name_text, (
            f"Неверное имя пользователя. Ожидалось содержание: '{expected_name_part}', "
            f"Фактический текст: '{actual_user_name_text}'")

    def test_registration_with_invalid_email_format_shows_errors(self, driver):
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)
        # Тест регистрации с email не по маске *******@*******.***
        invalid_email = f"invalid_{int(time.time())}@test.r"
        password_value = "TestPassword123"

        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(invalid_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        email_error = wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_ERROR_CONTAINER))
        password_error = driver.find_element(*RegistrationLocators.PASSWORD_ERROR_CONTAINER)
        confirm_password_error = driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_ERROR_CONTAINER)
        error_message_element = driver.find_element(*RegistrationLocators.EMAIL_ERROR_MESSAGE)

        is_email_red = email_error.is_displayed()
        is_password_red = password_error.is_displayed()
        is_confirm_red = confirm_password_error.is_displayed()
        actual_error_text = error_message_element.text
        expected_error_text = "Ошибка"

        assert is_email_red is True, "Поле Email не выделилось красным цветом при ошибке"
        assert is_password_red is True, "Поле Пароль не выделилось красным цветом при ошибке"
        assert is_confirm_red is True, "Поле Подтверждение пароля не выделилось красным цветом при ошибке"
        assert actual_error_text == expected_error_text, f"Неверный текст ошибки под полем Email. Ожидалось: '{expected_error_text}'"


    def test_registration_already_existing_user_shows_errors(self, driver):
        # Тест регистрации уже существующего пользователя.
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Вызываем метод генерации данных напрямую из модуля helpers
        user_data = generate_random_user_credentials()
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
