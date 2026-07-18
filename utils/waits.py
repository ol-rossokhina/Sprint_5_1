import time

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
Обёртки над явными ожиданиями Selenium (WebDriverWait).

Вместо time.sleep() и implicitly_wait() везде используются явные
ожидания конкретного условия с таймаутом.
"""

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
