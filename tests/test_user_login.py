from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators
from tests.helpers import generate_random_user_credentials


class TestUserLogin:
    # Тесты лежат в отдельном классе и отдельном модуле

    def test_user_successful_login(self, driver):
        # Тест успешного входа зарегистрированного пользователя
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Вызываем метод генерации данных напрямую из модуля helpers
        user_data = generate_random_user_credentials()
        unique_email = user_data["email"]
        password_value = user_data["password"]

        # Шаг 1. Предусловие: Регистрация пользователя, чтобы данные появились в БД
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(unique_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Ждем завершения регистрации, выходим из аккаунта для проверки чистого логина
        wait.until(EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))
        profile_btn = driver.find_element(*RegistrationLocators.USER_AVATAR)
        driver.execute_script("arguments[0].click();", profile_btn)
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGOUT_BUTTON)).click()

        # Шаг 2. Авторизация под созданным пользователем
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()

        # Заполняем форму авторизации корректными данными из хелпера
        email_field = wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(unique_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(password_value)

        # Отправляем форму авторизации
        driver.find_element(*RegistrationLocators.LOGIN_SUBMIT_BUTTON).click()

        # Шаг 3. Получение элементов для проверки фактического результата входа
        is_add_btn_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.ADD_AD_BUTTON)
        ).is_displayed()

        is_avatar_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR)
        ).is_displayed()

        user_name_element = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_NAME_HEADER)
        )
        is_name_visible = user_name_element.is_displayed()
        actual_name_text = user_name_element.text

        # Финальные однозначные ассерты со сравнением результатов согласно требованиям проекта
        assert is_add_btn_visible is True, "Кнопка размещения объявления не появилась"
        assert is_avatar_visible is True, "Аватар пользователя не отображается в шапке"
        assert is_name_visible is True, "Имя пользователя отсутствует на странице профиля"
        assert len(actual_name_text) > 0, f"Ожидалось заполненное имя пользователя, но поле пустое: '{actual_name_text}'"
