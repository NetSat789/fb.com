"""
Base Page class providing common page interactions.
All page objects should inherit from this class.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all Page Objects with common helper methods."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url, wait_until="domcontentloaded")

    def get_title(self) -> str:
        """Get the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Get the current URL."""
        return self.page.url

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def take_screenshot(self, name: str):
        """Take a screenshot and save to screenshots directory."""
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)

    def get_element_text(self, selector: str) -> str:
        """Get text content of an element."""
        return self.page.locator(selector).text_content() or ""

    def is_element_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.locator(selector).is_visible()
