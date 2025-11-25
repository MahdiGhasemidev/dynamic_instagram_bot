import time
from selenium.webdriver.common.by import By

def check_for_reply_notifications(driver):
    driver.get("https://www.instagram.com/accounts/activity/")
    time.sleep(4)

    target_text = "replied to your comment"
    items = driver.find_elements(By.CSS_SELECTOR, "div[role='button']")

    for item in items:
        try:
            text = item.text.lower()
            if target_text in text:
                item.click()
                time.sleep(3)
                return extract_reply_comment(driver)
        except:
            continue
    return None

def extract_reply_comment(driver):
    time.sleep(3)
    comments = driver.find_elements(By.CSS_SELECTOR, "ul li")

    for li in comments:
        text = li.text.strip()
        if "@" in text:
            return text
    return None