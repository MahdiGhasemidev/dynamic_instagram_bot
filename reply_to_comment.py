import time
from selenium.webdriver.common.by import By

def load_all_comments(driver):
    while True:
        try:
            more_btns = driver.find_elements(By.XPATH, "//span[contains(text(),'View') or contains(text(),'more')]")
            if not more_btns:
                break
            for btn in more_btns:
                try:
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)
                except:
                    pass
            time.sleep(1)
        except:
            break

def reply_to_specific_comment(driver, post_url, target_comment_text, reply_text):
    driver.get(post_url)
    time.sleep(4)

    load_all_comments(driver)
    time.sleep(2)

    all_comments = driver.find_elements(By.CSS_SELECTOR, "ul li")
    target_element = None

    for li in all_comments:
        try:
            t = li.text.strip()
            if target_comment_text.lower() in t.lower():
                target_element = li
                break
        except:
            continue

    if not target_element:
        print("❌ Comment not found.")
        return False

    try:
        reply_btn = target_element.find_element(By.XPATH, ".//button[contains(text(),'Reply')]")
        reply_btn.click()
        time.sleep(1)

        textarea = driver.find_element(By.CSS_SELECTOR, "form textarea")
        textarea.send_keys(reply_text)
        time.sleep(1)

        post_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
        post_btn.click()

        print(f"✅ Reply posted: {reply_text}")
        return True

    except Exception as e:
        print("❌ Failed to reply:", e)
        return False