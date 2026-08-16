import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AdsLocators
from tests.helpers import generate_random_user_credentials

class TestCreateAdvertisement:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_authenticated_user_can_create_ad_successfully(self, driver):
        # Тест успешного создания объявления авторизованным пользователем.
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Вызываем метод генерации данных напрямую из модуля helpers
        user_data = generate_random_user_credentials()
        unique_email = user_data["email"]
        password_value = user_data["password"]

        ad_title = f"{int(time.time())} Вилы"
        ad_description = "Прочные кованые вилы для работы в саду. Надежная ручка."
        ad_price = 1500

        # Шаг 1. Открываем форму и регистрируем нового уникального пользователя
        wait.until(EC.element_to_be_clickable(AdsLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(AdsLocators.NO_ACCOUNT_BUTTON)).click()

        # Заполняем форму регистрации
        wait.until(EC.visibility_of_element_located(AdsLocators.EMAIL_INPUT)).send_keys(unique_email)
        driver.find_element(*AdsLocators.PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*AdsLocators.REGISTER_CONFIRM_PASSWORD_INPUT).send_keys(password_value)
        driver.find_element(*AdsLocators.REGISTER_SUBMIT_BUTTON).click()

        # Ожидаем завершения регистрации (пользователь автоматически становится авторизованным)
        wait.until(EC.visibility_of_element_located(AdsLocators.USER_AVATAR))

        # Шаг 2. Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(AdsLocators.ADD_AD_BUTTON)).click()

        # Шаг 3. Заполнить все поля формы создания объявления
        # Заполнение названия
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
        publish_btn.click()

        # Важное умное ожидание: ждем, пока форма отправится и кнопка публикации исчезнет или станет невидимой
        wait.until(EC.invisibility_of_element_located(AdsLocators.PUBLISH_BUTTON))

        # Шаг 5. Перейти в профиль пользователя
        # Прямой переход на страницу профиля через принудительное обновление URL — самый надежный способ для React-приложений
        profile_url = f"{base_url}profile"
        driver.get(profile_url)

        # Шаг 6. Получение элементов для проверки фактического результата в блоке «Мои объявления»
        wait.until(EC.visibility_of_element_located(AdsLocators.MY_ADS_TITLE))

        # Ожидаем появление созданной карточки в блоке объявлений профиля
        created_ad_element = wait.until(EC.presence_of_element_located(AdsLocators.ANY_AD_CARD_TITLE))
        is_ad_visible = created_ad_element.is_displayed()

        # Финальный ассерт со сравнением фактического и ожидаемого результатов
        assert is_ad_visible is True, "Созданное объявление не появилось в блоке 'Мои объявления' личного кабинета"


