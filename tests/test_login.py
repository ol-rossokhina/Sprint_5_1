from data.auth_data import EXPECTED_USER_NAME
from locators.auth_locators import AuthModalLocators, HeaderLocators
from utils.waits import click, wait_clickable, wait_visible


class TestLogin:
    """Тесты на функциональность «Login пользователя»."""

    def test_successful_login(self, driver, registered_user):
        # После регистрации пользователь уже авторизован — выходим,
        # чтобы проверить именно сценарий входа по логину/паролю.
        click(driver, HeaderLocators.LOGOUT_BUTTON)

        click(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)
        wait_clickable(driver, AuthModalLocators.LOGIN_EMAIL_INPUT).send_keys(registered_user["email"])
        driver.find_element(*AuthModalLocators.LOGIN_PASSWORD_INPUT).send_keys(registered_user["password"])
        click(driver, AuthModalLocators.LOGIN_SUBMIT_BUTTON)

        actual_user_name = wait_visible(driver, HeaderLocators.USER_NAME_LABEL).text

        assert actual_user_name == EXPECTED_USER_NAME, (
            f"Ожидалось имя пользователя '{EXPECTED_USER_NAME}', фактическое значение: '{actual_user_name}'"
        )
