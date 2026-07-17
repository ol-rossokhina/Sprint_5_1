"""
Конфигурация окружения для запуска тестов: базовый URL сервиса,
путь для сохранения артефактов упавших тестов и настройка chromedriver.
"""

import os
from pathlib import Path

from selenium.webdriver.chrome.service import Service

BASE_URL = "https://qa-desk.education-services.ru/"

# Папка, куда сохраняются скриншот и HTML-дамп страницы при падении теста
# (см. хук pytest_runtest_makereport в conftest.py).
FAILURES_DIR = Path(__file__).resolve().parent.parent / "test-failures"

# --- Путь к chromedriver ---------------------------------------------------
CHROMEDRIVER_PATH = r"C:\Users\Rossokhina Olga\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"


def build_chrome_service() -> Service | None:
    """
    Возвращает Service с явно указанным путём к chromedriver, если
    CHROMEDRIVER_PATH задан, иначе None (тогда Selenium Manager
    попробует найти/скачать драйвер самостоятельно).
    """
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
