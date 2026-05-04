"""
Data-Driven Login Tests for Facebook Login Page.

Uses pytest.mark.parametrize with test data loaded from JSON/CSV files.
Covers positive, negative, and security test scenarios.
"""

import pytest
from pages.login_page import LoginPage
from utils.data_reader import DataReader


# ─── Load Test Data ────────────────────────────────────────
login_data = DataReader.get_login_test_data(source="json")
test_ids = DataReader.get_test_ids(login_data)


# ─── Data-Driven Login Tests ──────────────────────────────

class TestFacebookLogin:
    """Data-driven test suite for Facebook login functionality."""

    @pytest.mark.login
    @pytest.mark.parametrize("data", login_data, ids=test_ids)
    def test_login(self, login_page: LoginPage, data: dict):
        """
        Data-driven login test that handles all test scenarios.

        Args:
            login_page: LoginPage fixture (auto-navigated to FB).
            data: Dictionary with test data from JSON/CSV.
        """
        email = data["email"]
        password = data["password"]
        expected_result = data["expected_result"]
        test_id = data["test_id"]
        description = data["description"]

        print(f"\n🧪 Running: [{test_id}] {description}")

        # Perform login
        login_page.login(email, password)

        # Wait for page response
        login_page.page.wait_for_timeout(3000)

        # Assert based on expected result
        if expected_result == "login_success":
            # Successful login should redirect away from login page
            assert login_page.is_url_changed(), (
                f"[{test_id}] Expected URL to change after successful login"
            )

        elif expected_result == "login_failure":
            # Failed login should show error or remain on login/error page
            current_url = login_page.get_url()
            has_error = login_page.is_error_displayed()
            url_indicates_failure = (
                "login" in current_url.lower()
                or "checkpoint" in current_url.lower()
                or "recover" in current_url.lower()
            )

            assert has_error or url_indicates_failure, (
                f"[{test_id}] Expected login failure indication"
            )

            # Check specific error message if provided
            expected_msg = data.get("expected_message", "")
            if expected_msg:
                actual_msg = login_page.get_error_message()
                assert expected_msg.lower() in actual_msg.lower(), (
                    f"[{test_id}] Expected message '{expected_msg}' "
                    f"not found in '{actual_msg}'"
                )

        elif expected_result == "validation_error":
            # Validation errors keep user on the same page
            assert login_page.is_login_page_displayed() or "facebook.com" in login_page.get_url(), (
                f"[{test_id}] Expected to remain on login page for validation error"
            )


# ─── Filtered Test Suites ─────────────────────────────────
# These provide focused test runs for specific test types.

positive_data = DataReader.filter_by_type(login_data, "positive")
positive_ids = DataReader.get_test_ids(positive_data)

negative_data = DataReader.filter_by_type(login_data, "negative")
negative_ids = DataReader.get_test_ids(negative_data)

security_data = DataReader.filter_by_type(login_data, "security")
security_ids = DataReader.get_test_ids(security_data)


class TestPositiveLogin:
    """Positive login test scenarios only."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("data", positive_data, ids=positive_ids)
    def test_positive_login(self, login_page: LoginPage, data: dict):
        """Test valid login scenarios."""
        login_page.login(data["email"], data["password"])
        login_page.page.wait_for_timeout(3000)
        assert login_page.is_url_changed(), (
            f"[{data['test_id']}] Valid login should redirect away from login page"
        )


class TestNegativeLogin:
    """Negative login test scenarios only."""

    @pytest.mark.regression
    @pytest.mark.parametrize("data", negative_data, ids=negative_ids)
    def test_negative_login(self, login_page: LoginPage, data: dict):
        """Test invalid login scenarios."""
        login_page.login(data["email"], data["password"])
        login_page.page.wait_for_timeout(3000)

        current_url = login_page.get_url()
        still_on_login = (
            login_page.is_login_page_displayed()
            or "login" in current_url.lower()
            or "checkpoint" in current_url.lower()
        )
        assert still_on_login, (
            f"[{data['test_id']}] Invalid login should not redirect to home"
        )


class TestSecurityLogin:
    """Security-related login test scenarios."""

    @pytest.mark.regression
    @pytest.mark.parametrize("data", security_data, ids=security_ids)
    def test_security_login(self, login_page: LoginPage, data: dict):
        """Test security attack scenarios (e.g., SQL injection)."""
        login_page.login(data["email"], data["password"])
        login_page.page.wait_for_timeout(3000)

        # Security attacks should never result in successful login
        assert not login_page.is_url_changed() or "checkpoint" in login_page.get_url(), (
            f"[{data['test_id']}] Security attack should not bypass login"
        )
