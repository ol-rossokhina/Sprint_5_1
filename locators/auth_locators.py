"""
Локаторы элементов, связанных с авторизацией и регистрацией пользователя.

"""

from selenium.webdriver.common.by import By


class HeaderLocators:
    # Кнопка в шапке сайта, открывающая модальное окно входа/регистрации
    LOGIN_OR_REGISTER_BUTTON = (By.XPATH, "//button[contains(., 'Вход и регистрация')]")

    # Кнопка "Разместить объявление" в шапке сайта
    PLACE_AD_BUTTON = (By.XPATH, "//button[contains(., 'Разместить объявление')]")

    # Кнопка выхода из аккаунта
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(., 'Выйти')]")

    # Аватар пользователя (иконка-svg) рядом с кнопкой "Разместить объявление"
    USER_AVATAR = (By.CSS_SELECTOR, "svg.svgSmall")

    # Имя пользователя рядом с аватаром.
    USER_NAME_LABEL = (By.CSS_SELECTOR, "h3.profileText")


class AuthModalLocators:
    # Ссылка/кнопка переключения на форму регистрации внутри модального окна
    NO_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(., 'Нет аккаунта')]")

    # Поля формы авторизации
    LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    LOGIN_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")

    # Поля формы регистрации
    REGISTER_EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    REGISTER_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    REGISTER_REPEAT_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Повторите пароль']")
    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Создать аккаунт')]")

    # Сообщение об ошибке под полем Email.
    EMAIL_ERROR_MESSAGE = (
        By.XPATH,
        "//div[contains(@class, 'input_inputError')][.//input[@name='email']]"
        "/parent::div/parent::div/span[contains(@class, 'input_span')]",
    )

    # Признак ошибки (подсветка красным).
    EMAIL_FIELD_ERROR_STATE = (
        By.XPATH, "//div[contains(@class, 'input_inputError')][.//input[@name='email']]"
    )
    PASSWORD_FIELD_ERROR_STATE = (
        By.XPATH, "//div[contains(@class, 'input_inputError')][.//input[@name='password']]"
    )
    REPEAT_PASSWORD_FIELD_ERROR_STATE = (
        By.XPATH,
        "//div[contains(@class, 'input_inputError')][.//input[@placeholder='Повторите пароль']]",
    )


class NotAuthorizedModalLocators:
    # Модальное окно, которое появляется при попытке разместить объявление без авторизации
    AUTH_REQUIRED_MODAL_TITLE = (
        By.XPATH,
        "//*[contains(text(), 'Чтобы разместить объявление, авторизуйтесь')]",
    )
