import os
from pathlib import Path

from selenium.webdriver.chrome.service import Service

BASE_URL = "https://qa-desk.education-services.ru/"

# Папка, куда сохраняются скриншот и HTML-дамп страницы при падении теста
# (см. хук pytest_runtest_makereport в conftest.py).
FAILURES_DIR = Path(__file__).resolve().parent.parent / "test-failures"

# --- Путь к chromedriver ---------------------------------------------------
# Если Selenium Manager не может сам скачать chromedriver (нет сети,
# антивирус/прокси блокируют скачивание и т.п.), укажи путь к заранее
# скачанному chromedriver.exe через переменную окружения CHROMEDRIVER_PATH
# перед запуском pytest (в той же сессии терминала). Абсолютный путь
# НЕЛЬЗЯ хардкодить прямо в этом файле — он специфичен для конкретной
# машины и не будет работать ни у кого другого (в том числе на CI):
#   PowerShell:  $env:CHROMEDRIVER_PATH="C:\webdrivers\chromedriver.exe"
#   cmd:         set CHROMEDRIVER_PATH=C:\webdrivers\chromedriver.exe
#   Linux/macOS: export CHROMEDRIVER_PATH=/usr/local/bin/chromedriver
CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")


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
