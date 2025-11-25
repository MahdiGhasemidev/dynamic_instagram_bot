from login_with_cookies import login_with_cookies
from check_notifications import check_for_reply_notifications
from reply_to_comment import reply_to_specific_comment  # فقط برای تست

def select_accounts(accounts):
    print("\n=== Accounts List ===")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. {acc['username']}  |  {acc.get('email','')}")
    selected = input("\nEnter account numbers separated by comma (e.g., 1,2): ")
    indexes = [int(i.strip())-1 for i in selected.split(",")]
    return [accounts[i] for i in indexes if 0 <= i < len(accounts)]

def account_menu(driver, username):
    while True:
        print(f"\n--- Menu for {username} ---")
        print("1. Check notifications (reply to your comment)")
        print("2. Exit")
        choice = input("Select an action: ").strip()

        if choice == "1":
            reply_text = check_for_reply_notifications(driver)
            if reply_text:
                print("🟢 Reply detected:")
                print(reply_text)
                # برای تست، هنوز از GPT استفاده نمی‌کنیم
                post_url = input("Enter the post URL to reply on (for testing): ")
                reply_text_manual = input("Enter reply text manually (for testing): ")
                reply_to_specific_comment(driver, post_url, reply_text, reply_text_manual)
            else:
                print("⭕ No new reply notifications.")

        elif choice == "2":
            print(f"Exiting menu for {username}")
            break
        else:
            print("Invalid choice, try again.")

def main():
    import json
    ACCOUNTS_FILE = "data/accounts.json"
    with open(ACCOUNTS_FILE,"r",encoding="utf-8") as f:
        data = json.load(f)
    accounts = data.get("accounts", [])

    selected_accounts = select_accounts(accounts)
    drivers = []

    # Login all selected accounts
    for acc in selected_accounts:
        username = acc["username"]
        print(f"\nLogging in with cookies: {username}")
        driver = login_with_cookies(username)
        if driver:
            drivers.append((username, driver))

    # Menu for each logged in account
    for username, driver in drivers:
        account_menu(driver, username)

    # Close all drivers at the end
    for _, driver in drivers:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()