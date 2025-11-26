import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_comment(driver, target_text):
    spans = driver.find_elements(By.CSS_SELECTOR, "ul li span")
    for span in spans:
        try:
            text = span.text.strip()
            if text and target_text in text:
                print("🔍 Possible match:", text[:40])
                return span
        except:
            pass
    return None

def scroll_comment_box(driver, comment_box):
    try:
        driver.execute_script("arguments[0].scrollTop += 600;", comment_box)
        time.sleep(0.4)
        return True
    except Exception as e:
        print("⚠️ Could not scroll comment box:", e)
        return False

def reply_to_specific_comment(driver, post_url, target_comment, reply_text):
    driver.get(post_url)
    time.sleep(3)

    # پیدا کردن container کامنت‌ها به صورت داینامیک
    comment_box = None
    ul_elements = driver.find_elements(By.TAG_NAME, "ul")
    for ul in ul_elements:
        try:
            if len(ul.find_elements(By.TAG_NAME, "li")) > 0:
                comment_box = ul
                break
        except:
            continue

    if not comment_box:
        raise Exception("❌ No comment container found! IG UI may have changed.")

    # اسکرول و پیدا کردن کامنت هدف
    print("🔄 Scanning for target comment...")
    comment_element = None
    for _ in range(35):
        comment_element = find_comment(driver, target_comment)
        if comment_element:
            print("✅ Comment found!")
            break
        scroll_comment_box(driver, comment_box)
    else:
        print("❌ Could not find the comment in DOM.")
        return False

    # پیدا کردن دکمه Reply
    try:
        reply_btn = comment_element.find_element(By.XPATH, ".//button[contains(text(),'Reply') or contains(.,'Reply')]")
    except:
        try:
            reply_btn = comment_element.find_element(By.XPATH, ".//span[contains(text(),'Reply') or contains(.,'Reply')]")
        except:
            print("❌ Could not find Reply button near comment.")
            return False

    driver.execute_script("arguments[0].click();", reply_btn)
    time.sleep(0.8)

    # پیدا کردن textarea
    try:
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[aria-label='Add a reply…'], textarea"))
        )
    except:
        print("❌ Could not locate reply textarea.")
        return False

    # تایپ ریپلای
    driver.execute_script("arguments[0].value='';", textarea)
    time.sleep(0.2)
    for ch in reply_text:
        textarea.send_keys(ch)
        time.sleep(0.05)
    driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", textarea)
    time.sleep(0.5)

    # ارسال
    try:
        post_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Post']"))
        )
        driver.execute_script("arguments[0].click();", post_btn)
    except:
        print("❌ Could not click Post button.")
        return False

    print("✅ Reply posted successfully!")
    return True