import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

ACCOUNTS_FILE = "data/accounts.json"
COOKIES_DIR = "data/cookies"

# ایجاد پوشه کوکی‌ها اگر وجود ندارد
os.makedirs(COOKIES_DIR, exist_ok=True)


# ========================= LOAD ACCOUNTS =========================

def load_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "accounts" in data:
        return data["accounts"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("❌ ساختار فایل accounts.json صحیح نیست.")


# ========================= CHOOSE ACCOUNT =========================

def choose_account(accounts):
    print("accounts:\n")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. {acc['username']}  |  {acc['email']}")
    
    index = int(input("\n Enter the number of the account: ")) - 1

    if index < 0 or index >= len(accounts):
        raise ValueError("❌ شماره انتخاب شده صحیح نیست.")

    return accounts[index]


# ========================= CREATE DRIVER =========================

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


# ========================= OPEN BROWSER & SAVE COOKIES =========================

def open_browser_and_save_cookies_for(account):
    username = account["username"]

    driver = create_driver()
    driver.get("https://www.instagram.com/")
    
    print(f"\nChrome is now running for {username}. Please log in manually...")
    input("👉 After you finish login, press ENTER here to save cookies... ")

    # گرفتن کوکی‌ها
    cookies = driver.get_cookies()

    cookie_file = os.path.join(COOKIES_DIR, f"{username}_cookies.json")

    with open(cookie_file, "w", encoding="utf-8") as f:
        json.dump({
            "username": username,
            "cookies": cookies
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Cookies saved for {username} → {cookie_file}")

    time.sleep(2)
    driver.quit()


# ========================= MAIN =========================

if __name__ == "__main__":
    accounts = load_accounts()
    selected_account = choose_account(accounts)
    open_browser_and_save_cookies_for(selected_account)