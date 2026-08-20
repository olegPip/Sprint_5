from selenium.webdriver.common.by import By


class RegistrationLocators:
    # Кнопки для открытия формы
    # Поиск кнопки по тексту внутри тега
    LOGIN_REG_BUTTON = (By.XPATH, "//*[contains(text(), 'Вход и регистрация')]")
    NO_ACCOUNT_BUTTON = (By.XPATH, "//*[contains(text(), 'Нет аккаунта')]")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//form//button[@type='submit' and contains(text(), 'Войти')]")

    # Форма регистрации
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "submitPassword")
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//form//button[@type='submit' and contains(text(), 'Создать аккаунт')]")

    # Элементы личного кабинета (после успешного входа)
    USER_AVATAR = (By.CSS_SELECTOR, "button.circleSmall")
    USER_NAME_HEADER = (By.CSS_SELECTOR, "h3.profileText.name")
    ADD_AD_BUTTON = (By.XPATH, "//*[contains(text(), 'Разместить объявление')]")
    LOGOUT_BUTTON = (By.XPATH, "//*[contains(text(), 'Выйти')]")

    # Локаторы для проверки ошибок
    # Поля, выделенные красным (поиск по классу ошибки инпута)
    EMAIL_ERROR_CONTAINER = (By.CSS_SELECTOR, "div.input_inputError__fLUP9 input[name='email']")
    PASSWORD_ERROR_CONTAINER = (By.CSS_SELECTOR, "div.input_inputError__fLUP9 input[name='password']")
    CONFIRM_PASSWORD_ERROR_CONTAINER = (By.CSS_SELECTOR, "div.input_inputError__fLUP9 input[name='submitPassword']")

    # Текст сообщения об ошибке под полем Email
    EMAIL_ERROR_MESSAGE = (By.XPATH,
                           "//input[@name='email']/ancestor::div[2]/following-sibling::span[@class='input_span__yWPqB']")


class LoginLocators:
    # Кнопки для открытия и отправки формы
    LOGIN_REG_BUTTON = (By.XPATH, "//*[contains(text(), 'Вход и регистрация')]")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//form//button[@type='submit' and contains(text(), 'Войти')]")

    # Поля формы авторизации
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")

    # Элементы шапки после успешного Login (из предоставленного HTML)
    # Аватар пользователя (круглый элемент с SVG внутри)
    USER_AVATAR = (By.CSS_SELECTOR, "button.circleSmall")
    # Имя пользователя (h3 с классом name, содержащий текст "User.")
    USER_NAME_HEADER = (By.CSS_SELECTOR, "h3.profileText.name")
    # Кнопка «Разместить объявление»
    ADD_AD_BUTTON = (By.XPATH, "//button[contains(text(), 'Разместить объявление')]")
    # Кнопка Logout
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "button.spanGlobal.btnSmall")


class AdsLocators:
    # Элементы главной страницы
    # Кнопка «Разместить объявление» в шапке сайта
    ADD_AD_BUTTON = (By.XPATH, "//button[contains(text(), 'Разместить объявление')]")

    # Модальное окно авторизации
    AUTH_MODAL = (
        By.CSS_SELECTOR,
        "div[class*='homePage_modal']"
    )
    # Элементы модального окна авторизации
    # Заголовок модального окна
    AUTH_REQUIRED_MODAL_TITLE = (By.XPATH, "//h1[text()='Чтобы разместить объявление, авторизуйтесь']")

    # Локаторы авторизации (Предусловие)
    LOGIN_REG_BUTTON = (By.XPATH, "//*[contains(text(), 'Вход и регистрация')]")

    # Авторизация
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")

    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//form//button[@type='submit' and contains(text(), 'Войти')]")
    USER_AVATAR = (By.XPATH, "//div[contains(@class, 'flexRow')]//button[contains(@class, 'circleSmall')]")

    # Переход к регистрации
    NO_ACCOUNT_BUTTON = (By.XPATH, "//button[@type='button' and normalize-space()='Нет аккаунта']")

    # Регистрация
    REGISTER_CONFIRM_PASSWORD_INPUT = (By.NAME, "submitPassword")

    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Создать аккаунт']")

    # Поля формы создания объявления
    TITLE_INPUT = (By.NAME, "name")
    DESCRIPTION_INPUT = (By.XPATH, "//*[@placeholder='Описание товара' or contains(@placeholder, 'Описание')]")
    PRICE_INPUT = (By.NAME, "price")

    # Выпадающие списки (Dropdown) и Radio
    CATEGORY_DROPDOWN = (By.NAME, "category")
    CITY_DROPDOWN = (By.NAME, "city")

    # Dropdown города
    CITY_OPTION = (By.XPATH, "//button[.//span[normalize-space()='Москва']]")

    # Элементы внутри открывшихся списков, по которым нужно кликнуть для выбора
    # Выбирает любой первый попавшийся элемент из выпадающего списка (li или div с текстом)
    CATEGORY_OPTION = (By.XPATH, "//button[.//span[normalize-space()='Садоводство']]")
    CONDITION_RADIO = (By.CSS_SELECTOR,"input[name='condition'][value='Новый']")

    # Кнопка публикации
    PUBLISH_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Опубликовать']")
    PROFILE_BUTTON = (By.CSS_SELECTOR, "button.circleSmall")

    # Блок «Мои объявления»
    MY_ADS_TITLE = (By.XPATH,"//h1[normalize-space()='Мои объявления']")


    # Локатор находит заголовок h2 любой карточки внутри блока объявлений профиля
    ANY_AD_CARD_TITLE = (By.XPATH, "//div[contains(@class, 'profilePage_listningBlock')]//div[contains(@class, 'card')]//h2")