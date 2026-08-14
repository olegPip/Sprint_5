from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import AdsLocators


class TestCreateAd:
    # Тесты лежат в отдельном классе и отдельном тестовом модуле

    def test_unauthorized_user_cannot_create_ad(self, driver):
        # Тест: Проверка вызова модального окна авторизации
        # при попытке создать объявление неавторизованным пользователем.
        base_url = "https://qa-desk.education-services.ru/"
        driver.get(base_url)
        wait = WebDriverWait(driver, 10)

        # Шаг 1. Нажать кнопку «Разместить объявление»
        wait.until(EC.element_to_be_clickable(AdsLocators.ADD_AD_BUTTON)).click()

        # Шаг 2. Получить элемент заголовка модального окна
        modal_title_element = wait.until(
            EC.visibility_of_element_located(AdsLocators.AUTH_REQUIRED_MODAL_TITLE)
        )

        # Шаг 3. Финальные ассерты (сравнение фактического и ожидаемого результатов)
        is_modal_visible = modal_title_element.is_displayed()
        actual_modal_text = modal_title_element.text
        expected_modal_text = "Чтобы разместить объявление, авторизуйтесь"

        # Проверка 1: Модальное окно действительно отображается на экране
        assert is_modal_visible is True, "Модальное окно авторизации не появилось на экране"

        # Проверка 2: Текст заголовка строго соответствует ожидаемому тексту по ТЗ
        assert actual_modal_text == expected_modal_text, (
            f"Текст заголовка не совпадает. "
            f"Ожидалось: '{expected_modal_text}', но получено: '{actual_modal_text}'")
