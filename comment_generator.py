from openai_client import chat_completion

# فایل پرامپت
PROMPT_FILE = "data/comment_prompt.txt"
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    BASE_PROMPT = f.read()


def generate_comment(video_topic: str) -> str:
    prompt = f"{BASE_PROMPT}\n\nموضوع ویدئو: {video_topic}\nلطفاً یک کامنت کوتاه، خودمونی، فارسی و طبیعی بنویس."
    return chat_completion(prompt)


def generate_reply(original_comment: str) -> str:
    prompt = f"{BASE_PROMPT}\n\nکاربر این کامنت را گذاشته: «{original_comment}»\nیک پاسخ کوتاه، دوستانه، فارسی و طبیعی بنویس."
    return chat_completion(prompt)