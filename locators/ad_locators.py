from selenium.webdriver.common.by import By

"""
Локаторы элементов формы создания объявления и страницы профиля пользователя.

"""


class CreateAdFormLocators:
    TITLE_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[name='description']")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[name='price']")

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

    @staticmethod
    def condition_radio_by_value(value: str):
        return (
            By.XPATH,
            f"//input[@name='condition'][@value='{value}']"
            "/ancestor::div[contains(@class, 'radioUnput_shell')]",
        )

    PUBLISH_BUTTON = (By.XPATH, "//button[contains(., 'Опубликовать')]")


class ProfileLocators:
    PROFILE_LINK = (By.CSS_SELECTOR, "button.circleSmall")

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
