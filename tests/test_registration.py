from locators.auth_locators import AuthModalLocators, HeaderLocators
from utils.waits import click, wait_clickable, wait_visible

PASSWORD = "Qwerty123!"
INVALID_EMAIL = "user_without_at_sign"


class TestRegistration:
    """Тесты на функциональность «Регистрация пользователя»."""

    def test_successful_registration(self, driver, generate_email):
        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

        wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(generate_email)
        driver.find_element(*AuthModalLocators.REGISTER_PASSWORD_INPUT).send_keys(PASSWORD)
        driver.find_element(*AuthModalLocators.REGISTER_REPEAT_PASSWORD_INPUT).send_keys(PASSWORD)
        click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

        actual_user_name = wait_visible(driver, HeaderLocators.USER_NAME_LABEL).text

        assert actual_user_name == "User.", (
            f"Ожидалось имя пользователя 'User.', фактическое значение: '{actual_user_name}'"
        )

    def test_registration_with_invalid_email_mask(self, driver):
        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        click(driver, AuthModalLocators.NO_ACCOUNT_BUTTON)

        wait_clickable(driver, AuthModalLocators.REGISTER_EMAIL_INPUT).send_keys(INVALID_EMAIL)
        click(driver, AuthModalLocators.REGISTER_SUBMIT_BUTTON)

        error_message_text = wait_visible(driver, AuthModalLocators.EMAIL_ERROR_MESSAGE).text

        assert error_message_text == "Ошибка", (
            f"Ожидалось сообщение об ошибке 'Ошибка', фактическое значение: '{error_message_text}'"
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

        assert error_message_text == "Ошибка", (
            f"Ожидалось сообщение об ошибке 'Ошибка', фактическое значение: '{error_message_text}'"
        )
