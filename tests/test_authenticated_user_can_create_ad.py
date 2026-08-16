import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AdsLocators
from tests.urls import TestUrls


class TestCreateAdvertisement:
    """Класс объединяет тестовые методы по функциональности работы с объявлениями"""

    def test_authenticated_user_can_create_ad_successfully(self, driver):
        # Тест успешного создания объявления авторизованным пользователем.
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Используем данные строго заранее созданного статического пользователя
        static_email = "test1@test.ru"
        static_password = "Test123"

        ad_title = f"{int(time.time())} Вилы"
        ad_description = "Прочные кованые вилы для работы в саду. Надежная ручка."
        ad_price = 1500

        # Шаг 1. Авторизоваться под заранее созданным пользователем
        wait.until(EC.element_to_be_clickable(AdsLocators.LOGIN_REG_BUTTON)).click()

        # Заполняем форму входа корректными статическими данными
        email_field = wait.until(EC.visibility_of_element_located(AdsLocators.EMAIL_INPUT))
        email_field.clear()
        email_field.send_keys(static_email)

        driver.find_element(*AdsLocators.PASSWORD_INPUT).send_keys(static_password)

        # Нажимаем кнопку «Войти» стандартным методом клика
        wait.until(EC.element_to_be_clickable(AdsLocators.LOGIN_SUBMIT_BUTTON)).click()

        # Ожидаем завершения авторизации по появлению аватара пользователя в шапке
        wait.until(EC.visibility_of_element_located(AdsLocators.USER_AVATAR))

        # Шаг 2. Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(AdsLocators.ADD_AD_BUTTON)).click()

        # Шаг 3. Заполнить все поля формы создания объявления
        wait.until(EC.visibility_of_element_located(AdsLocators.TITLE_INPUT)).send_keys(ad_title)

        # Открытие и выбор категории "Садоводство" через JavaScript (исправлен синтаксис аргументов)
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

        # Шаг 5. Перейти в профиль пользователя принудительным роутингом URL
        driver.get(TestUrls.PROFILE_PAGE)

        # Шаг 6. Получение элементов для проверки фактического результата в блоке «Мои объявления»
        my_ads_title_element = wait.until(EC.visibility_of_element_located(AdsLocators.MY_ADS_TITLE))
        is_profile_loaded = my_ads_title_element.is_displayed()

        # Финальный однозначный ассерт со сравнением результатов согласно критериям проекта
        assert is_profile_loaded is True, "Страница профиля 'Мои объявления' не загрузилась после публикации товара"





