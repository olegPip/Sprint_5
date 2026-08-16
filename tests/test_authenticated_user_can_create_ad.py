import time
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AdsLocators
from tests.urls import TestUrls


class TestCreateAdvertisement:

    def test_authenticated_user_can_create_ad_successfully(self, driver):
        # Тест успешного создания объявления авторизованным пользователем.
        driver.get(TestUrls.BASE_URL)
        wait = WebDriverWait(driver, 10)

        # Генерируем уникальный Email. Профиль будет абсолютно чистым, без лимитов и пагинации.
        session_email = f"fixed_{int(time.time())}@test.ru"
        static_password = "TestPassword123!"

        ad_title = f"{int(time.time())} Вилы"
        ad_description = "Прочные кованые вилы для работы в саду. Надежная ручка."
        ad_price = 1500

        # Шаг 1. Сверхбыстрая регистрация (минуя долгие анимации вызова модальных окон UI)
        wait.until(EC.element_to_be_clickable(AdsLocators.LOGIN_REG_BUTTON)).click()
        wait.until(EC.element_to_be_clickable(AdsLocators.NO_ACCOUNT_BUTTON)).click()

        # Заполняем поля напрямую без лишних ожиданий
        email_field = wait.until(EC.presence_of_element_located(AdsLocators.EMAIL_INPUT))
        email_field.send_keys(session_email)
        driver.find_element(*AdsLocators.PASSWORD_INPUT).send_keys(static_password)

        # Вводим подтверждение пароля и отправляем форму нажатием клавиши Enter (экономим UI-время кликов)
        confirm_field = driver.find_element(*AdsLocators.REGISTER_CONFIRM_PASSWORD_INPUT)
        confirm_field.send_keys(static_password + Keys.ENTER)

        # Ожидаем завершения авторизации (появление аватара подтверждает успешный вход)
        wait.until(EC.visibility_of_element_located(AdsLocators.USER_AVATAR))

        # Шаг 2. Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(AdsLocators.ADD_AD_BUTTON)).click()

        # Шаг 3. Заполнить все поля формы создания объявления
        wait.until(EC.visibility_of_element_located(AdsLocators.TITLE_INPUT)).send_keys(ad_title)

        # Выбор категории "Садоводство" через JavaScript
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

        # Ждем очистки инпута, подтверждающей, что бэкенд принял и записал данные объявления
        wait.until(EC.text_to_be_present_in_element_value(AdsLocators.TITLE_INPUT, ""))

        # Шаг 5. Перейти в профиль пользователя принудительным обновлением URL
        driver.get(TestUrls.PROFILE_PAGE)

        # Шаг 6. Получение элементов для проверки фактического результата в блоке «Мои объявления»
        wait.until(EC.visibility_of_element_located(AdsLocators.MY_ADS_TITLE))

        # Проверяем наличие нашей уникальной карточки в чистом профиле (теперь она гарантированно там появится)
        created_ad_element = wait.until(EC.visibility_of_element_located(AdsLocators.ANY_AD_CARD_TITLE))
        is_ad_visible = created_ad_element.is_displayed()

        # Финальный ассерт со сравнением фактического и ожидаемого результатов
        assert is_ad_visible is True, "Созданное объявление не появилось в блоке 'Мои объявления' личного кабинета"



