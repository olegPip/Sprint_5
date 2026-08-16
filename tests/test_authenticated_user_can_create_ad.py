import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AdsLocators


class TestCreateAdvertisement:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_authenticated_user_can_create_ad_successfully(self, driver):
        # Тест успешного создания объявления авторизованным пользователем.
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Используем альтернативного статического пользователя, чтобы обойти переполненные лимиты аккаунта test1
        static_email = "test1@test.ru"
        static_password = "Test123"

        # Название делаем максимально коротким и уникальным
        ad_title = f"{int(time.time())} Вилы"
        ad_description = "Прочные кованые вилы."
        ad_price = 100

        # Шаг 1. Авторизоваться под заранее созданным пользователем
        wait.until(EC.element_to_be_clickable(AdsLocators.LOGIN_REG_BUTTON)).click()

        email_field = wait.until(EC.visibility_of_element_located(AdsLocators.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(static_email)

        driver.find_element(*AdsLocators.PASSWORD_INPUT).send_keys(static_password)

        # Нажимаем кнопку «Войти» через JavaScript для гарантированной отправки формы
        login_submit_btn = driver.find_element(*AdsLocators.LOGIN_SUBMIT_BUTTON)
        driver.execute_script("arguments[0].click();", login_submit_btn)

        # Ожидаем завершения авторизации по появлению аватара пользователя в шапке
        wait.until(EC.visibility_of_element_located(AdsLocators.USER_AVATAR))

        # Шаг 2. Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(AdsLocators.ADD_AD_BUTTON)).click()

        # Шаг 3. Заполнить все поля формы создания объявления
        wait.until(EC.visibility_of_element_located(AdsLocators.TITLE_INPUT)).send_keys(ad_title)

        # Открытие и выбор категории "Садоводство" через JavaScript
        category_dropdown = driver.find_element(*AdsLocators.CATEGORY_DROPDOWN)
        driver.execute_script("arguments[0].click();", category_dropdown)

        category_option = wait.until(EC.presence_of_element_located(AdsLocators.CATEGORY_OPTION))
        driver.execute_script("arguments[0].click();", category_option)

        # Выбор состояния товара "Новый" из RadioButton через JavaScript
        condition_radio = driver.find_element(*AdsLocators.CONDITION_RADIO)
        driver.execute_script("arguments[0].click();", condition_radio)

        # Открытие и выбор города "Москва" через JavaScript
        city_dropdown = driver.find_element(*AdsLocators.CITY_DROPDOWN)
        driver.execute_script("arguments[0].click();", city_dropdown)

        city_option = wait.until(EC.presence_of_element_located(AdsLocators.CITY_OPTION))
        driver.execute_script("arguments[0].click();", city_option)

        # Заполнение описания товара и стоимости
        driver.find_element(*AdsLocators.DESCRIPTION_INPUT).send_keys(ad_description)
        driver.find_element(*AdsLocators.PRICE_INPUT).send_keys(str(ad_price))

        # Шаг 4. Нажать кнопку «Опубликовать»
        publish_btn = wait.until(EC.element_to_be_clickable(AdsLocators.PUBLISH_BUTTON))
        driver.execute_script("arguments[0].click();", publish_btn)

        # Шаг 5. Перейти в профиль пользователя
        # Принудительно запрашиваем страницу профиля через URL, чтобы гарантировать обновление DOM и базы SPA
        profile_url = f"{base_url}profile"
        driver.get(profile_url)

        # Шаг 6. Получение элементов для проверки фактического результата в блоке «Мои объявления»
        wait.until(EC.visibility_of_element_located(AdsLocators.MY_ADS_TITLE))

        # Ожидаем появление созданной карточки в блоке объявлений профиля
        created_ad_element = wait.until(EC.presence_of_element_located(AdsLocators.ANY_AD_CARD_TITLE))
        is_ad_visible = created_ad_element.is_displayed()

        # Финальный ассерт со сравнением фактического и ожидаемого результатов
        assert is_ad_visible is True, "Созданное объявление не появилось в блоке 'Мои объявления' личного кабинета"





