"""
Pytest conftest.py - Shared fixtures for all tests.
Manages browser lifecycle, page objects, and screenshot capture on failure.
"""

import os
import pytest
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.config_reader import ConfigReader
from pages.login_page import LoginPage


# ─── Directories ───────────────────────────────────────────
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
REPORTS_DIR = Path(__file__).parent / "reports"

SCREENSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)


# ─── Browser & Context Fixtures ───────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    """Launch a browser instance for the entire test session."""
    with sync_playwright() as p:
        browser_type = ConfigReader.get_browser()
        launcher = getattr(p, browser_type)

        browser = launcher.launch(
            headless=ConfigReader.is_headless(),
            slow_mo=ConfigReader.get_slow_mo(),
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser_instance, request):
    """
    Create a new browser context and page for each test.
    Captures screenshot on test failure.
    """
    viewport = ConfigReader.get_viewport()
    context = browser_instance.new_context(
        viewport=viewport,
        ignore_https_errors=True,
    )
    context.set_default_timeout(ConfigReader.get_timeout())

    page = context.new_page()
    yield page

    # Screenshot on failure
    if request.node.rep_call and request.node.rep_call.failed:
        if ConfigReader.should_screenshot_on_failure():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name.replace("[", "_").replace("]", "")
            screenshot_path = SCREENSHOTS_DIR / f"FAIL_{test_name}_{timestamp}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

    context.close()


@pytest.fixture(scope="function")
def login_page(page):
    """Provide a LoginPage object navigated to the Facebook login page."""
    lp = LoginPage(page)
    lp.open()
    return lp


# ─── Pytest Hooks ──────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result on the item for screenshot capture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
