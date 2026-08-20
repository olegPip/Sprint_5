import time
import pytest
from selenium import webdriver


# Создание и закрытие браузера
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Инициализируем браузер
    browser = webdriver.Chrome(options=options)

    yield browser  # Передаем браузер в тесты и другие фикстуры

    browser.quit()  # Закрываем после окончания теста


