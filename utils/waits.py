"""
Обёртки над явными ожиданиями Selenium (WebDriverWait).

Сайт — React SPA, поэтому элементы появляются/пропадают асинхронно,
а иногда пересоздаются в DOM (например, при переключении формы логина
на форму регистрации внутри одного модального окна). Чтобы такие
перерисовки не приводили к StaleElementReferenceException, это
исключение явно игнорируется в ожидании — Selenium просто повторно
ищет элемент на следующей итерации вместо падения.

Вместо time.sleep() и implicitly_wait() везде используются явные
ожидания конкретного условия с таймаутом.
"""

import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10
IGNORED_EXCEPTIONS = (StaleElementReferenceException,)


def wait_visible(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.visibility_of_element_located(locator)
    )


def wait_clickable(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.element_to_be_clickable(locator)
    )


def wait_present(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.presence_of_element_located(locator)
    )


def wait_invisible(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.invisibility_of_element_located(locator)
    )


def wait_url_contains(driver, url_part: str, timeout: int = DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout, ignored_exceptions=IGNORED_EXCEPTIONS).until(
        EC.url_contains(url_part)
    )


def click(driver, locator, timeout: int = DEFAULT_TIMEOUT):
    """
    Дожидается кликабельности элемента и кликает по нему.

    В отличие от `wait_clickable(driver, locator).click()`, эта функция
    устойчива к ситуации, когда React перерисовывает DOM ровно в момент
    между тем, как элемент найден, и тем, как выполняется сам клик
    (например, сразу после навигации/сабмита формы). Если в момент клика
    ссылка на элемент оказывается "протухшей" (StaleElementReferenceException),
    элемент ищется заново и клик повторяется — в пределах общего таймаута.
    """
    end_time = time.monotonic() + timeout
    last_exception = None

    while time.monotonic() < end_time:
        remaining = max(1, int(end_time - time.monotonic()))
        try:
            element = wait_clickable(driver, locator, timeout=remaining)
            element.click()
            return element
        except StaleElementReferenceException as exc:
            last_exception = exc

    raise TimeoutException(f"Не удалось кликнуть по элементу: {locator}") from last_exception
