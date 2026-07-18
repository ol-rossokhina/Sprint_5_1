import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.config import BASE_URL, FAILURES_DIR, build_chrome_service


@pytest.fixture
def driver():
    """
    Поднимает экземпляр Chrome WebDriver перед тестом и открывает базовую
    страницу сервиса. После завершения теста браузер закрывается.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    chrome_service = build_chrome_service()

    if chrome_service:
        chrome_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    else:
        chrome_driver = webdriver.Chrome(options=chrome_options)

    chrome_driver.get(BASE_URL)

    yield chrome_driver

    chrome_driver.quit()



@pytest.fixture
def registered_user(driver):
    """
    Создаёт нового пользователя через форму регистрации и возвращает
    его учётные данные. Используется тестами, которым для проверки
    нужен уже существующий в системе аккаунт (логин, повторная
    регистрация, логаут, создание объявления).
    """
    from data.auth_data import VALID_PASSWORD
    from helpers.email_helpers import generate_email
    from locators.auth_locators import AuthModalLocators, HeaderLocators
    from utils.waits import click, wait_clickable

    email = generate_email()
    password = VALID_PASSWORD

    click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
    click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

    wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(email)
    driver.find_element(*AuthModalLocators.REGISTER_PASSWORD_INPUT).send_keys(password)
    driver.find_element(*AuthModalLocators.REGISTER_REPEAT_PASSWORD_INPUT).send_keys(password)
    click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

    wait_clickable(driver, HeaderLocators.USER_NAME_LABEL)

    return {"email": email, "password": password}


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
