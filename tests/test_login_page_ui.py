"""
Tests for Facebook Login Page UI elements.
Validates that all expected UI elements are present and correctly configured.
"""

import pytest
from pages.login_page import LoginPage


class TestLoginPageUI:
    """Test suite for verifying login page UI elements."""

    @pytest.mark.smoke
    def test_page_title(self, login_page: LoginPage):
        """Verify the page title contains 'Facebook'."""
        title = login_page.get_page_title()
        assert "facebook" in title.lower(), f"Expected 'Facebook' in title, got: {title}"

    @pytest.mark.smoke
    def test_email_field_visible(self, login_page: LoginPage):
        """Verify the email input field is visible."""
        assert login_page.is_email_field_visible(), "Email field is not visible"

    @pytest.mark.smoke
    def test_password_field_visible(self, login_page: LoginPage):
        """Verify the password input field is visible."""
        assert login_page.is_password_field_visible(), "Password field is not visible"

    @pytest.mark.smoke
    def test_login_button_visible(self, login_page: LoginPage):
        """Verify the login button is visible."""
        assert login_page.is_login_button_visible(), "Login button is not visible"

    @pytest.mark.smoke
    def test_email_placeholder(self, login_page: LoginPage):
        """Verify the email field has a placeholder text."""
        placeholder = login_page.get_email_placeholder()
        assert len(placeholder) > 0, "Email field placeholder is empty"

    @pytest.mark.smoke
    def test_password_placeholder(self, login_page: LoginPage):
        """Verify the password field has a placeholder text."""
        placeholder = login_page.get_password_placeholder()
        assert len(placeholder) > 0, "Password field placeholder is empty"
