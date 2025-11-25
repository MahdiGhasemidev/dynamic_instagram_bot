import json
import os
import time
from selenium import webdriver

ACCOUNTS_FILE = "data/accounts.json"
COOKIES_DIR   = "data/cookies"

# ================== Load Accounts ==================
def load_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "accounts" in data:
        return data["accounts"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("❌ accounts.json format is invalid.")


# ================== Choose Account =================
def choose_account(accounts):
    print("Accounts available:\n")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. {acc['username']}  |  {acc['email']}")
    
    index = int(input("\nEnter the number of the account to login: ")) - 1
    if index < 0 or index >= len(accounts):
        raise ValueError("❌ Invalid account selection.")
    return accounts[index]


# ================== Load Cookies ===================
def load_cookies(username):
    path = os.path.join(COOKIES_DIR, f"{username}_cookies.json")
    if not os.path.exists(path):
        print(f"❌ Cookies not found for {username}.")
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # If saved format is {"username": "...", "cookies": [...]}
    if isinstance(data, dict) and "cookies" in data:
        return data["cookies"]

    # Otherwise assume list of cookies
    return data

# ================== Create Driver ==================
def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver


# ================== Login with Cookies =============
def login_with_cookies(username):
    cookies = load_cookies(username)
    if not cookies:
        return
    
    driver = create_driver()
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Add cookies
    for cookie in cookies:
        c = {
            "name": cookie.get("name"),
            "value": cookie.get("value"),
            "domain": cookie.get("domain", ".instagram.com"),
            "path": cookie.get("path", "/"),
            "secure": cookie.get("secure", True),
            "httpOnly": cookie.get("httpOnly", False),
        }
        try:
            driver.add_cookie(c)
        except Exception:
            pass

    # Refresh to login
    driver.refresh()
    time.sleep(5)

    print(f"✅ Logged in to {username} successfully.")

    return driver


# ================== MAIN ============================
if __name__ == "__main__":
    accounts = load_accounts()
    selected_account = choose_account(accounts)
    login_with_cookies(selected_account["username"])
    
    print("⚠️ Browser will remain open. Close it manually or press Ctrl+C.")