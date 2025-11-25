from login_with_cookies import login_with_cookies
import json
import time

ACCOUNTS_FILE = "data/accounts.json"


def load_accounts():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def launch_multiple(accounts_to_run=None):
    """
    accounts_to_run = list of usernames, or None → run all
    """
    accounts = load_accounts()

    if accounts_to_run is None:
        target_accounts = accounts
    else:
        target_accounts = [a for a in accounts if a["username"] in accounts_to_run]

    active = []

    for acc in target_accounts:
        username = acc["username"]
        print(f"\n➡️ Starting browser session for: {username}")
        driver = login_with_cookies(username)
        if driver:
            active.append(driver)
            print(f"🟢 {username} is now online.")
        time.sleep(2)

    print("\nAll selected accounts are online.")

    try:
        while True:
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nClosing all browsers...")
        for d in active:
            try:
                d.quit()
            except:
                pass


if __name__ == "__main__":
    # Example: run only specific accounts
    usernames = [
        "alinazari9491",
        # "other_username",
    ]
    launch_multiple(usernames)