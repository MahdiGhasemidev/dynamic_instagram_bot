from gpt_client import chat_completion

def generate_comment(video_topic):
    prompt = f"""
شما یک کامنت فارسی خودمونی و دوستانه برای یک پست اینستاگرام تولید می‌کنید.
شرایط:
- خودمونی و راحت باشد
- حداکثر ۲ جمله
- متن کوتاه و طبیعی باشد
موضوع پست:
{video_topic}

کامنت مناسب را بنویس:
"""
    return chat_completion(prompt)


def generate_reply(user_comment):
    prompt = f"""
شما یک ریپلای فارسی خودمونی و دوستانه برای یک کامنت اینستاگرام تولید می‌کنید.
شرایط:
- خودمونی و راحت
- کوتاه و طبیعی
کامنت اصلی:
{user_comment}

ریپلای مناسب را بنویس:
"""
    return chat_completion(prompt)