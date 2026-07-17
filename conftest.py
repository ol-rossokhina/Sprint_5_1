import os
import uuid
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = "https://qa-desk.education-services.ru/"
FAILURES_DIR = Path(__file__).parent / "test-failures"

# --- Путь к chromedriver ---------------------------------------------------
# Если Selenium Manager не может сам скачать chromedriver (нет сети,
# антивирус/прокси блокируют скачивание (не знаю, по какой причине у меня не получилось) и т.п.), указала путь к заранее
# скачанному chromedriver.exe через переменную CHROMEDRIVER_PATH

CHROMEDRIVER_PATH = r"C:\Users\Rossokhina Olga\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"


def _build_chrome_service() -> Service | None:
    if not CHROMEDRIVER_PATH:
        return None

    driver_path = Path(CHROMEDRIVER_PATH)
    if not driver_path.is_file():
        raise FileNotFoundError(
            f"CHROMEDRIVER_PATH указывает на несуществующий файл: '{CHROMEDRIVER_PATH}'. "
            "Проверь, что путь указывает именно на chromedriver.exe (после распаковки архива), "
            "а не на папку или на .zip."
        )

    return Service(executable_path=str(driver_path))


@pytest.fixture
def driver():
    """
    Поднимает экземпляр Chrome WebDriver перед тестом и открывает базовую
    страницу сервиса. После завершения теста браузер закрывается.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    chrome_service = _build_chrome_service()

    if chrome_service:
        chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    else:
        chrome_driver = webdriver.Chrome(options=chrome_options)

    chrome_driver.get(BASE_URL)

    yield chrome_driver

    chrome_driver.quit()


@pytest.fixture
def generate_email():
    """
    Генерирует уникальный email на каждый вызов, чтобы тесты регистрации
    не конфликтовали с уже существующими в системе пользователями.
    """
    unique_part = uuid.uuid4().hex[:10]
    return f"user_{unique_part}@example.com"


@pytest.fixture
def registered_user(driver, generate_email):
    """
    Создаёт нового пользователя через форму регистрации и возвращает
    его учётные данные. Используется тестами, которым для проверки
    нужен уже существующий в системе аккаунт (логин, повторная
    регистрация, логаут, создание объявления).
    """
    from data.auth_data import VALID_PASSWORD
    from locators.auth_locators import AuthModalLocators, HeaderLocators
    from utils.waits import click, wait_clickable

    password = VALID_PASSWORD

    click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
    click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

    wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(generate_email)
    driver.find_element(*AuthModalLocators.REGISTER_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthModalLocators.REGISTER_REPEAT_PASSWORD_INPUT).send_keys(password)
    click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

    wait_clickable(driver, HeaderLocators.USER_NAME_LABEL)

    return {"email": generate_email, "password": password}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Если тест упал, сохраняет скриншот и HTML-дамп страницы на момент
    падения в папку test-failures/. Это помогает быстро понять, что
    реально отображалось в браузере, не перезапуская тест вручную.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when not in ("call", "setup") or not report.failed:
        return

    driver_instance = item.funcargs.get("driver")
    if driver_instance is None:
        return

    FAILURES_DIR.mkdir(exist_ok=True)
    safe_test_name = item.nodeid.replace("::", "__").replace("/", "__").replace("\\", "__")

    screenshot_path = FAILURES_DIR / f"{safe_test_name}.png"
    html_path = FAILURES_DIR / f"{safe_test_name}.html"

    try:
        driver_instance.save_screenshot(str(screenshot_path))
        html_path.write_text(driver_instance.page_source, encoding="utf-8")
    except Exception:
        # Если браузер уже закрыт/недоступен — просто пропускаем сохранение.
        pass
