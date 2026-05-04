"""
Login Page Object for Facebook Login Page.
Contains all locators and actions related to the Facebook login page.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Facebook Login Page."""

    # ─── URL ───────────────────────────────────────────────
    URL = "https://www.facebook.com"

    # ─── Locators ──────────────────────────────────────────
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#pass"
    LOGIN_BUTTON = 'button[name="login"]'
    FORGOT_PASSWORD_LINK = 'a[href*="recover"]'
    CREATE_ACCOUNT_BUTTON = 'a[data-testid="open-registration-form-button"]'
    ERROR_MESSAGE = "div._9ay7"  # Facebook error message container
    LOGIN_FORM = "#loginform"
    FB_LOGO = 'img[alt*="Facebook"]'

    def __init__(self, page: Page):
        super().__init__(page)

    # ─── Navigation ────────────────────────────────────────

    def open(self):
        """Navigate to the Facebook login page."""
        self.navigate(self.URL)
        return self

    # ─── Actions ───────────────────────────────────────────

    def enter_email(self, email: str):
        """Enter email or phone number in the email field."""
        self.page.locator(self.EMAIL_INPUT).click()
        self.page.locator(self.EMAIL_INPUT).fill(email)
        return self

    def enter_password(self, password: str):
        """Enter password in the password field."""
        self.page.locator(self.PASSWORD_INPUT).click()
        self.page.locator(self.PASSWORD_INPUT).fill(password)
        return self

    def click_login(self):
        """Click the login button."""
        self.page.locator(self.LOGIN_BUTTON).click()
        return self

    def click_forgot_password(self):
        """Click the 'Forgotten password?' link."""
        self.page.locator(self.FORGOT_PASSWORD_LINK).click()
        return self

    def click_create_account(self):
        """Click the 'Create new account' button."""
        self.page.locator(self.CREATE_ACCOUNT_BUTTON).click()
        return self

    def login(self, email: str, password: str):
        """
        Perform a complete login action.

        Args:
            email: The email/phone to enter.
            password: The password to enter.
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self

    # ─── Assertions / Getters ──────────────────────────────

    def get_error_message(self) -> str:
        """Get the error message text displayed after failed login."""
        try:
            self.page.wait_for_selector(self.ERROR_MESSAGE, timeout=10000)
            return self.get_element_text(self.ERROR_MESSAGE)
        except Exception:
            return ""

    def is_login_page_displayed(self) -> bool:
        """Check if the login page is displayed."""
        return self.page.locator(self.EMAIL_INPUT).is_visible()

    def is_email_field_visible(self) -> bool:
        """Check if the email input field is visible."""
        return self.page.locator(self.EMAIL_INPUT).is_visible()

    def is_password_field_visible(self) -> bool:
        """Check if the password input field is visible."""
        return self.page.locator(self.PASSWORD_INPUT).is_visible()

    def is_login_button_visible(self) -> bool:
        """Check if the login button is visible."""
        return self.page.locator(self.LOGIN_BUTTON).is_visible()

    def is_error_displayed(self) -> bool:
        """Check if an error message is displayed."""
        try:
            self.page.wait_for_selector(self.ERROR_MESSAGE, timeout=5000)
            return self.page.locator(self.ERROR_MESSAGE).is_visible()
        except Exception:
            return False

    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.get_title()

    def get_email_placeholder(self) -> str:
        """Get the placeholder text of the email field."""
        return self.page.locator(self.EMAIL_INPUT).get_attribute("placeholder") or ""

    def get_password_placeholder(self) -> str:
        """Get the placeholder text of the password field."""
        return self.page.locator(self.PASSWORD_INPUT).get_attribute("placeholder") or ""

    def is_url_changed(self) -> bool:
        """Check if URL has changed from the login page (indicating navigation)."""
        current_url = self.get_url()
        return current_url != self.URL and "facebook.com" in current_url
