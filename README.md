# UI-автотесты для qa-desk.education-services.ru

Набор UI-автотестов на Selenium + pytest для учебного сервиса объявлений
[qa-desk.education-services.ru](https://qa-desk.education-services.ru/).

Покрыта функциональность:

- Регистрация пользователя (успешная регистрация, email не по маске,
  повторная регистрация уже существующего пользователя).
- Login пользователя.
- Logout пользователя.
- Создание объявления (неавторизованным и авторизованным пользователем).

## Структура проекта

```
Sprint_5/
├── conftest.py              # общие фикстуры: driver, генерация email, registered_user
├── locators/
│   ├── auth_locators.py     # локаторы шапки сайта, форм входа/регистрации
│   └── ad_locators.py       # локаторы формы создания объявления и профиля
├── utils/
│   └── waits.py             # обёртки над явными ожиданиями (WebDriverWait)
├── tests/
│   ├── test_registration.py
│   ├── test_login.py
│   ├── test_logout.py
│   └── test_ad_creation.py
├── requirements.txt
├── pytest.ini
└── .gitignore
```

## Требования

- Python 3.10+
- Google Chrome (актуальной версии) и соответствующий ему chromedriver,
  доступный в PATH, либо управляемый через Selenium Manager (входит в
  Selenium 4.20+, поэтому отдельная установка драйвера обычно не требуется).

## Установка

```bash
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск тестов

Запуск всего набора:

```bash
pytest
```

Запуск конкретного файла:

```bash
pytest tests/test_registration.py
```

Запуск с подробным выводом:

```bash
pytest -v
```

## Принципы, заложенные в проект

- Каждый тест независим: сам открывает браузер (фикстура `driver`),
  выполняет проверку и закрывает браузер (`driver.quit()` в teardown фикстуры).
- Для тестов, которым нужен уже зарегистрированный пользователь, используется
  фикстура `registered_user`, которая перед тестом регистрирует нового
  пользователя с уникальным email.
- Email для регистрации генерируется заново в каждом тесте (фикстура
  `generate_email`) во избежание конфликтов с уже существующими аккаунтами.
- Локаторы не хранятся внутри тестов — они вынесены в модуль `locators`.
- Вместо `time.sleep()` и `implicitly_wait()` используются явные ожидания
  (`WebDriverWait`) из `utils/waits.py`.

