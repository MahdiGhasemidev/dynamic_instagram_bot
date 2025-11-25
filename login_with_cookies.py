import json
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

COOKIES_DIR = "data/cookies"


def create_driver():
    """Create Chrome driver with standard settings."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    return driver


def load_cookies(username):
    """Load cookies from file."""
    path = os.path.join(COOKIES_DIR, f"{username}_cookies.json")

    if not os.path.exists(path):
        print(f"❌ Cookies not found for {username}.")
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("cookies")


def login_with_cookies(username):
    """Open browser and login using saved cookies."""

    cookies = load_cookies(username)
    if not cookies:
        return None

    driver = create_driver()
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Add cookies
    for cookie in cookies:
        try:
            c = {
                "name": cookie["name"],
                "value": cookie["value"],
                "path": cookie.get("path", "/"),
                "domain": cookie.get("domain", ".instagram.com"),
                "secure": cookie.get("secure", True),
                "httpOnly": cookie.get("httpOnly", False),
            }

            # Instagram requires being on the right domain before adding cookies
            driver.add_cookie(c)

        except Exception as e:
            # Ignore invalid cookies (sessionid always works)
            pass

    # Refresh → login happens automatically
    driver.refresh()
    time.sleep(4)

    print(f"🟢 Logged in with cookies as: {username}")

    return driver