"""
Локаторы элементов формы создания объявления и страницы профиля пользователя.

См. примечание в auth_locators.py про необходимость сверки с реальным DOM.
"""

from selenium.webdriver.common.by import By


class CreateAdFormLocators:
    # Поле "Название" — реальный HTML-атрибут name="name" (placeholder "Название")
    TITLE_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[name='description']")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[name='price']")

    # Dropdown "Категория" — кастомный компонент: клик по readonly-инпуту
    # список НЕ открывает, список открывается кликом по кнопке-стрелке,
    # которая идёт следующим соседним элементом за инпутом.
    CATEGORY_TOGGLE = (
        By.XPATH,
        "//input[@name='category']/following-sibling::button[contains(@class, 'dropDownMenu_arrowDown')]",
    )

    @staticmethod
    def category_option_by_text(option_text: str):
        return (
            By.XPATH,
            "//input[@name='category']"
            "/ancestor::div[contains(@class, 'dropDownMenu_dropMenu')]"
            f"//button[.//span[normalize-space(text())='{option_text}']]",
        )

    # Dropdown "Город" — аналогичный компонент, отличается только name="city"
    CITY_TOGGLE = (
        By.XPATH,
        "//input[@name='city']/following-sibling::button[contains(@class, 'dropDownMenu_arrowDown')]",
    )

    @staticmethod
    def city_option_by_text(option_text: str):
        return (
            By.XPATH,
            "//input[@name='city']"
            "/ancestor::div[contains(@class, 'dropDownMenu_dropMenu')]"
            f"//button[.//span[normalize-space(text())='{option_text}']]",
        )

    # RadioButton "Состояние товара" — сам <input> визуально скрыт
    # (кастомный радиобаттон), поэтому кликаем по видимому родительскому
    # блоку, а не по самому input, чтобы избежать перехвата клика.
    @staticmethod
    def condition_radio_by_value(value: str):
        return (
            By.XPATH,
            f"//input[@name='condition'][@value='{value}']"
            "/ancestor::div[contains(@class, 'radioUnput_shell')]",
        )

    PUBLISH_BUTTON = (By.XPATH, "//button[contains(., 'Опубликовать')]")


class ProfileLocators:
    # Переход в профиль пользователя — кликабельна именно кнопка с аватаром
    # (button.circleSmall), а не сам текст имени (h3.profileText), который
    # является статичным текстом без обработчика клика.
    PROFILE_LINK = (By.CSS_SELECTOR, "button.circleSmall")

    # Блок "Мои объявления" на странице профиля.
    # Реальная разметка: <h1>Мои объявления</h1> внутри
    # <div class="profilePage_listningBlock__..."> (тега <section> на странице нет).
    MY_ADS_SECTION = (
        By.XPATH,
        "//h1[contains(text(), 'Мои объявления')]"
        "/ancestor::div[contains(@class, 'profilePage_listningBlock')][1]",
    )

    # Карточка объявления внутри блока "Мои объявления" по заголовку
    @staticmethod
    def ad_card_by_title(title: str):
        return (
            By.XPATH,
            "//h1[contains(text(), 'Мои объявления')]"
            "/ancestor::div[contains(@class, 'profilePage_listningBlock')][1]"
            f"//*[contains(text(), '{title}')]",
        )
