from locators.auth_locators import HeaderLocators
from utils.waits import click, wait_invisible, wait_visible


class TestLogout:
    """Тесты на функциональность «Logout пользователя»."""

    def test_successful_logout(self, driver, registered_user):
        click(driver, HeaderLocators.LOGOUT_BUTTON)

        wait_invisible(driver, HeaderLocators.USER_NAME_LABEL)
        login_button = wait_visible(driver, HeaderLocators.LOGIN_OR_REGISTER_BUTTON)

        assert login_button.is_displayed(), (
            "Ожидалось отображение кнопки 'Вход и регистрация' после выхода из аккаунта"
        )
