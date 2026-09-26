import re

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

URGENT_KEYWORDS = [
    "click here", "verify your account", "verify your identity",
    "confirm your identity", "account suspended", "account locked",
    "you've won", "claim your prize", "act now", "limited time offer",
    "urgent action required", "unusual login", "suspicious activity detected",
    "wire transfer", "social security number",
]

def count_urls(text: str) -> int:
    return len(URL_PATTERN.findall(text))


def has_url(text: str) -> int:
    return 1 if count_urls(text) > 0 else 0


def count_urgent_keywords(text: str) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(keyword) for keyword in URGENT_KEYWORDS)


def extract_features(text: str) -> dict:
    url_present = has_url(text)
    url_count = count_urls(text)
    urgent_count = count_urgent_keywords(text)

    urgent_and_url = 1 if (url_present and urgent_count > 0) else 0

    return {
        "has_url": url_present,
        "url_count": url_count,
        "urgent_keyword_count": urgent_count,
        "urgent_and_url": urgent_and_url,
    }

