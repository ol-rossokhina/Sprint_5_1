import uuid

from locators.ad_locators import CreateAdFormLocators, ProfileLocators
from locators.auth_locators import HeaderLocators, NotAuthorizedModalLocators
from utils.waits import click, wait_clickable, wait_visible

AD_DESCRIPTION = "Автотест: описание товара"
AD_PRICE = "1000"
AD_CATEGORY = "Книги"
AD_CITY = "Санкт-Петербург"
AD_CONDITION_VALUE = "Б/У"


class TestAdCreation:
    """Тесты на функциональность «Создание объявления»."""

    def test_create_ad_by_unauthorized_user(self, driver):
        click(driver, HeaderLocators.PLACE_AD_BUTTON)

        modal_title = wait_visible(driver, NotAuthorizedModalLocators.AUTH_REQUIRED_MODAL_TITLE)

        assert modal_title.is_displayed(), (
            "Ожидалось модальное окно с заголовком "
            "'Чтобы разместить объявление, авторизуйтесь'"
        )

    def test_create_ad_by_authorized_user(self, driver, registered_user):
        ad_title = f"Автотест объявление {uuid.uuid4().hex[:8]}"

        click(driver, HeaderLocators.PLACE_AD_BUTTON)

        wait_clickable(driver, CreateAdFormLocators.TITLE_INPUT).send_keys(ad_title)
        driver.find_element(*CreateAdFormLocators.DESCRIPTION_INPUT).send_keys(AD_DESCRIPTION)
        driver.find_element(*CreateAdFormLocators.PRICE_INPUT).send_keys(AD_PRICE)

        click(driver, CreateAdFormLocators.CATEGORY_TOGGLE)
        click(driver, CreateAdFormLocators.category_option_by_text(AD_CATEGORY))

        click(driver, CreateAdFormLocators.CITY_TOGGLE)
        click(driver, CreateAdFormLocators.city_option_by_text(AD_CITY))

        click(driver, CreateAdFormLocators.condition_radio_by_value(AD_CONDITION_VALUE))

        click(driver, CreateAdFormLocators.PUBLISH_BUTTON)

        click(driver, ProfileLocators.PROFILE_LINK)

        created_ad_locator = ProfileLocators.ad_card_by_title(ad_title)
        created_ad_card = wait_visible(driver, created_ad_locator)

        assert created_ad_card.is_displayed(), (
            f"Ожидалось, что объявление '{ad_title}' отображается в блоке 'Мои объявления'"
        )
