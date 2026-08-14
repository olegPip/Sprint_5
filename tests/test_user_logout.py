from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators


class TestUserLogout:

    def test_user_successful_logout(self, driver, random_user_credentials):
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Данные из независимой фикстуры
        valid_email = random_user_credentials["email"]
        valid_password = random_user_credentials["password"]

        # ШАГ 1: РЕГИСТРАЦИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(valid_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(valid_password)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(valid_password)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Проверяем, что регистрация прошла и мы внутри (виден аватар)
        wait.until(EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))

        # ШАГ 2: ВЫХОД (LOGOUT)
        # 1. Сначала кликаем по аватару, чтобы открылось меню пользователя
        wait.until(EC.element_to_be_clickable(RegistrationLocators.USER_AVATAR)).click()

        # 2. Теперь кликаем по появившейся кнопке «Выйти»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGOUT_BUTTON)).click()

        # ШАГ 3: ПРОВЕРКА РЕЗУЛЬТАТА
        # Проверяем, что кнопка «Вход и регистрация» снова на месте
        is_login_button_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.LOGIN_REG_BUTTON)
        ).is_displayed()

        # Проверяем, что элементы ЛК скрылись
        is_avatar_hidden = wait.until(
            EC.invisibility_of_element_located(RegistrationLocators.USER_AVATAR)
        )

        # Явные ассерты согласно требованиям вашего проекта
        assert is_login_button_visible is True, "Кнопка входа не появилась после логаута"
        assert is_avatar_hidden is True, "Аватар пользователя остался видимым после логаута"
