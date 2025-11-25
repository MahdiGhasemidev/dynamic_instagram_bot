import json
import time
from login_with_cookies import login_with_cookies
from check_notifications import check_for_reply_notifications
from reply_to_comment import reply_to_specific_comment
from comment_generator import generate_comment, generate_reply
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ---------------- Account Selection ---------------- #
def select_accounts(accounts):
    print("\n=== Accounts List ===")
    for i, acc in enumerate(accounts):
        print(f"{i+1}. {acc['username']}  |  {acc.get('email','')}")
    selected = input("\nEnter account numbers separated by comma (e.g., 1,2): ")
    indexes = [int(i.strip())-1 for i in selected.split(",")]
    return [accounts[i] for i in indexes if 0 <= i < len(accounts)]

# ---------------- Human-like Typing ---------------- #
def human_type_textarea(driver, textarea, text, delay=0.08):
    actions = ActionChains(driver)
    textarea.click()
    for ch in text:
        actions.send_keys(ch).pause(delay)
    actions.perform()

# ---------------- Stable Human-like Comment ---------------- #
def comment_on_post_human(driver, post_url, comment_text, timeout=15, retries=3):
    """
    Human-like typing + safe Post click
    """
    driver.get(post_url)
    time.sleep(2)  # wait for post to load

    for attempt in range(retries):
        try:
            # Locate textarea
            textarea = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Add a comment…']"))
            )

            # Remove non-BMP characters to avoid Chrome emoji issues
            safe_text = ''.join(c for c in comment_text if ord(c) <= 0xFFFF)

            # Clear existing text
            driver.execute_script("arguments[0].value = '';", textarea)
            time.sleep(0.2)

            # Human-like typing
            human_type_textarea(driver, textarea, safe_text)

            # Dispatch input event for React
            driver.execute_script("""
                var ta = arguments[0];
                ta.dispatchEvent(new Event('input', { bubbles: true }));
            """, textarea)

            # Wait a few seconds after typing to ensure React updates
            time.sleep(1.0)

            # Locate Post button
            post_btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                    "div.xdj266r.x1xegmmw.xat24cr.x13fj5qh div[role='button'][tabindex='0']"))
            )

            # Scroll + JS click
            driver.execute_script("arguments[0].scrollIntoView({block:'center'}); arguments[0].click();", post_btn)
            time.sleep(1)
            print("✅ Comment posted successfully!")
            return True

        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(1)

    print("❌ Failed to post comment after multiple attempts.")
    return False

# ---------------- Account Menu ---------------- #
def account_menu(driver, username):
    while True:
        print(f"\n--- Menu for {username} ---")
        print("1. Check notifications (reply to your comment)")
        print("2. Comment on a post (manual or AI)")
        print("3. Reply to specific comment (manual or AI)")
        print("4. Exit this account")

        choice = input("Select an action: ").strip()

        if choice == "1":
            reply_info = check_for_reply_notifications(driver)
            if not reply_info:
                print("⭕ No new reply notifications found.")
                continue
            original_comment, reply_text = reply_info
            print(f"\n🟢 New reply detected:\nYour comment: {original_comment}\nReply: {reply_text}")
            post_url = input("Enter post URL to reply: ").strip()
            reply_to_specific_comment(driver, post_url, reply_text, "Test reply")
            print("✅ Replied successfully.")

        elif choice == "2":
            post_url = input("Enter post URL: ").strip()
            method = input("Manual comment or AI? (m/a): ").lower()

            if method == "m":
                manual_text = input("Enter your comment text: ")
                comment_on_post_human(driver, post_url, manual_text)
            elif method == "a":
                video_topic = input("Describe the video topic (in Persian): ").strip()
                print("Generating AI comment...")
                ai_comment = generate_comment(video_topic)
                print("\n🔵 AI Comment:")
                print(ai_comment)
                confirm = input("Send comment? (y/n): ").lower()
                if confirm == "y":
                    comment_on_post_human(driver, post_url, ai_comment)
                else:
                    print("❌ Canceled.")
            else:
                print("Invalid choice, try again.")

        elif choice == "3":
            post_url = input("Enter post URL: ").strip()
            target_comment = input("Enter the comment you want to reply to: ").strip()
            method = input("Manual reply or AI? (m/a): ").lower()

            if method == "m":
                reply_text = input("Enter reply text: ")
                reply_to_specific_comment(driver, post_url, target_comment, reply_text)
                print("✅ Reply posted.")
            elif method == "a":
                ai_reply = generate_reply(target_comment)
                print("\n🔵 AI Reply:")
                print(ai_reply)
                confirm = input("Send reply? (y/n): ").lower()
                if confirm == "y":
                    reply_to_specific_comment(driver, post_url, target_comment, ai_reply)
                    print("✅ Reply posted.")
                else:
                    print("❌ Canceled.")
            else:
                print("Invalid choice, try again.")

        elif choice == "4":
            print(f"Exiting menu for {username}")
            break
        else:
            print("Invalid choice, try again.")

# ---------------- MAIN ---------------- #
def main():
    ACCOUNTS_FILE = "data/accounts.json"
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
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

    # Menu for each logged-in account
    for username, driver in drivers:
        account_menu(driver, username)

    # Close all drivers
    for _, driver in drivers:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    main()