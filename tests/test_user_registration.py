import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators


class TestUserRegistration:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_user_registration_flow(self, driver):
        # Тест успешной регистрации нового пользователя.
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Email для тестов регистрации генерируется каждый раз новый
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
