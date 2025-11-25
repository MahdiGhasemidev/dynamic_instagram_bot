import time
from selenium.webdriver.common.by import By

def comment_on_post(driver, post_url, comment_text):
    driver.get(post_url)
    time.sleep(4)

    try:
        textarea = driver.find_element(By.CSS_SELECTOR, "form textarea")
        textarea.click()
        time.sleep(1)
        textarea.send_keys(comment_text)
        time.sleep(1)

        post_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
        post_btn.click()

        print(f"✅ Comment posted: {comment_text}")
        return True

    except Exception as e:
        print("❌ Failed to post comment:", e)
        return False