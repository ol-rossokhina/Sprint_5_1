import uuid

from data.ad_data import AD_CATEGORY, AD_CITY, AD_CONDITION_VALUE, AD_DESCRIPTION, AD_PRICE, AD_TITLE_PREFIX
from locators.ad_locators import CreateAdFormLocators, ProfileLocators
from locators.auth_locators import HeaderLocators, NotAuthorizedModalLocators
from utils.waits import click, wait_clickable, wait_visible


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
        ad_title = f"{AD_TITLE_PREFIX} {uuid.uuid4().hex[:8]}"

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

        # После публикации сайт сам асинхронно редиректит на главную страницу.
        # Дожидаемся, что этот редирект точно завершился (шапка главной
        # страницы отрисовалась), прежде чем кликать по аватару — иначе
        # клик по профилю может произойти раньше и быть перезаписан
        # более поздним редиректом от самой публикации.
        wait_visible(driver, HeaderLocators.PLACE_AD_BUTTON)

        click(driver, ProfileLocators.PROFILE_LINK)

        created_ad_locator = ProfileLocators.ad_card_by_title(ad_title)
        created_ad_card = wait_visible(driver, created_ad_locator)

        assert created_ad_card.is_displayed(), (
            f"Ожидалось, что объявление '{ad_title}' отображается в блоке 'Мои объявления'"
        )
