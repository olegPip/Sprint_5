from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import RegistrationLocators  # Используем ваш единый класс локаторов


class TestUserLogin:
    # Тесты лежат в отдельном классе и отдельном модуле

    def test_user_successful_login(self, driver, random_user_credentials):
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Данные берутся из независимой фикстуры, email всегда новый
        valid_email = random_user_credentials["email"]
        valid_password = random_user_credentials["password"]

        # РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ (чтобы данные были в БД)
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.NO_ACCOUNT_BUTTON)).click()

        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(valid_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(valid_password)
        driver.find_element(*RegistrationLocators.CONFIRM_PASSWORD_INPUT).send_keys(valid_password)
        driver.find_element(*RegistrationLocators.CREATE_ACCOUNT_BUTTON).click()

        # Ждем успешного завершения регистрации и выходим, чтобы проверить чистый логин
        wait.until(EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR))
        wait.until(EC.element_to_be_clickable(RegistrationLocators.USER_AVATAR)).click()
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGOUT_BUTTON)).click()

        # ШАГ 1: АВТОРИЗАЦИЯ
        # Снова нажимаем кнопку «Вход и регистрация»
        wait.until(EC.element_to_be_clickable(RegistrationLocators.LOGIN_REG_BUTTON)).click()

        # Заполняем форму авторизации свежими данными
        wait.until(EC.visibility_of_element_located(RegistrationLocators.EMAIL_INPUT)).send_keys(valid_email)
        driver.find_element(*RegistrationLocators.PASSWORD_INPUT).send_keys(valid_password)

        # Нажимаем кнопку «Войти» (используем точный локатор)
        driver.find_element(*RegistrationLocators.LOGIN_SUBMIT_BUTTON).click()

        # ШАГ 2: ПРОВЕРКА РЕЗУЛЬТАТОВ
        # Проверяем появление кнопки «Разместить объявление»
        is_add_btn_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.ADD_AD_BUTTON)
        ).is_displayed()

        # Проверяем отображение аватара пользователя
        is_avatar_visible = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_AVATAR)
        ).is_displayed()

        # Проверяем отображение имени в заголовке профиля
        user_name_element = wait.until(
            EC.visibility_of_element_located(RegistrationLocators.USER_NAME_HEADER)
        )
        is_name_visible = user_name_element.is_displayed()
        actual_name_text = user_name_element.text

        # Сравнение фактического и ожидаемого результатов
        assert is_add_btn_visible is True, "Кнопка размещения объявления не появилась"
        assert is_avatar_visible is True, "Аватар пользователя не отображается в шапке"
        assert is_name_visible is True, "Имя пользователя отсутствует на странице профиля"

        # Если при регистрации имя по умолчанию создается пустое или совпадает с частью email, сверяем наличие текста
        assert len(actual_name_text) > 0, f"Ожидалось имя пользователя, но поле пустое: '{actual_name_text}'"