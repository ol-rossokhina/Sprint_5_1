from data.auth_data import EXPECTED_FORM_ERROR_MESSAGE, EXPECTED_USER_NAME, INVALID_EMAIL, VALID_PASSWORD
from helpers.email_helpers import generate_email
from locators.auth_locators import AuthModalLocators, HeaderLocators
from utils.waits import click, wait_clickable, wait_visible



class TestRegistration:
    """Тесты на функциональность «Регистрация пользователя»."""

    def test_successful_registration(self, driver):
        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

        wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(generate_email())
        driver.find_element(*AuthModalLocators.REGISTER_PASSWORD_INPUT).send_keys(VALID_PASSWORD)
        driver.find_element(*AuthModalLocators.REGISTER_REPEAT_PASSWORD_INPUT).send_keys(VALID_PASSWORD)
        click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

        actual_user_name = wait_visible(driver, HeaderLocators.USER_NAME_LABEL).text

        assert actual_user_name == EXPECTED_USER_NAME, (
            f"Ожидалось имя пользователя '{EXPECTED_USER_NAME}', фактическое значение: '{actual_user_name}'"
        )

    def test_registration_with_invalid_email_mask(self, driver):
        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

        wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(INVALID_EMAIL)
        click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

        error_message_text = wait_visible(driver, AuthModalLocators.EMAIL_ERROR_MESSAGE).text

        assert error_message_text == EXPECTED_FORM_ERROR_MESSAGE, (
            f"Ожидалось сообщение об ошибке '{EXPECTED_FORM_ERROR_MESSAGE}', фактическое значение: '{error_message_text}'"
        )

    def test_registration_of_existing_user(self, driver, registered_user):
        click(driver, HeaderLocators.LOGOUT_BUTTON)

        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

        wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(registered_user["email"])
        driver.find_element(*AuthModalLocators.REGISTER_PASSWORD_INPUT).send_keys(registered_user["password"])
        driver.find_element(*AuthModalLocators.REGISTER_REPEAT_PASSWORD_INPUT).send_keys(
            registered_user["password"]
        )
        click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

        error_message_text = wait_visible(driver, AuthModalLocators.EMAIL_ERROR_MESSAGE).text

        assert error_message_text == EXPECTED_FORM_ERROR_MESSAGE, (
            f"Ожидалось сообщение об ошибке '{EXPECTED_FORM_ERROR_MESSAGE}', фактическое значение: '{error_message_text}'"
        )
