"""
Configuration reader utility.
Loads and provides access to project configuration settings.
"""

import json
from pathlib import Path


class ConfigReader:
    """Reads and provides access to project configuration."""

    _config = None
    CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"

    @classmethod
    def _load_config(cls) -> dict:
        """Load configuration from JSON file (cached)."""
        if cls._config is None:
            with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
                cls._config = json.load(f)
        return cls._config

    @classmethod
    def get(cls, key: str, default=None):
        """Get a configuration value by key."""
        config = cls._load_config()
        return config.get(key, default)

    @classmethod
    def get_base_url(cls) -> str:
        return cls.get("base_url", "https://www.facebook.com")

    @classmethod
    def get_browser(cls) -> str:
        return cls.get("browser", "chromium")

    @classmethod
    def is_headless(cls) -> bool:
        return cls.get("headless", False)

    @classmethod
    def get_slow_mo(cls) -> int:
        return cls.get("slow_mo", 0)

    @classmethod
    def get_timeout(cls) -> int:
        return cls.get("timeout", 30000)

    @classmethod
    def get_viewport(cls) -> dict:
        return cls.get("viewport", {"width": 1280, "height": 720})

    @classmethod
    def should_screenshot_on_failure(cls) -> bool:
        return cls.get("screenshot_on_failure", True)
