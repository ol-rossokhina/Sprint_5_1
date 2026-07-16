"""
Локаторы элементов, связанных с авторизацией и регистрацией пользователя.

ВАЖНО: локаторы построены на основании видимого текста кнопок/заголовков
и стандартных атрибутов полей ввода (name / placeholder), так как точная
разметка сайта не проверялась в headless-окружении без браузера.
Перед первым запуском сверь их с реальным DOM через Chrome DevTools
(клик правой кнопкой на элементе -> "Просмотреть код") и при необходимости
поправь ТОЛЬКО в этом файле — тесты менять не нужно.
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
    # На сайте отображается как "User." (с точкой на конце) в теге <h3 class="profileText name">.
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
    REGISTER_REPEAT_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='submitPassword']")
    REGISTER_SUBMIT_BUTTON = (By.XPATH, "//button[contains(., 'Создать аккаунт')]")

    # Сообщение об ошибке под полем Email
    EMAIL_ERROR_MESSAGE = (
        By.XPATH,
        "//input[@name='email']/ancestor::*[contains(@class, 'field') or contains(@class, 'form-group')]"
        "//*[contains(text(), 'Ошибка')]",
    )

    # Признак ошибки (подсветка красным) для полей email/пароль/повтор пароля
    EMAIL_FIELD_ERROR_STATE = (By.CSS_SELECTOR, "input[name='email'].error, input[name='email'][class*='invalid']")
    PASSWORD_FIELD_ERROR_STATE = (
        By.CSS_SELECTOR,
        "input[name='password'].error, input[name='password'][class*='invalid']",
    )
    REPEAT_PASSWORD_FIELD_ERROR_STATE = (
        By.CSS_SELECTOR,
        "input[name='submitPassword'].error, input[name='submitPassword'][class*='invalid']",
    )


class NotAuthorizedModalLocators:
    # Модальное окно, которое появляется при попытке разместить объявление без авторизации
    AUTH_REQUIRED_MODAL_TITLE = (
        By.XPATH,
        "//*[contains(text(), 'Чтобы разместить объявление, авторизуйтесь')]",
    )
