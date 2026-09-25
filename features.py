import re

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

URGENT_KEYWORDS = [
    "urgent", "verify", "click here", "suspended", "immediately",
    "winner", "claim", "act now", "limited time", "confirm your",
    "update your", "password", "account locked",
    ]

def count_urls(text: str) -> int:
    return len(URL_PATTERN.findall(text))

def has_url(text: str) -> int:
    return 1 if count_urls(text) > 0 else 0

def count_urgent_keywords(text: str) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(keyword) for keyword in URGENT_KEYWORDS)

def extract_features(text: str) -> dict:
    return {
        "has_url" : has_url(text),
        "url_count" : count_urls(text),
        "urgent_keyword_count" : count_urgent_keywords(text),
        }

if __name__ == "__main__":
    sample = "Urgent! Your account will be suspended. Click here: http://fake-bank.com/login"
    print(extract_features(sample))
