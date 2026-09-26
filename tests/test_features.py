import unittest
from features import count_urls, has_url, count_urgent_keywords, extract_features
 
 
class TestFeatures(unittest.TestCase):
 
    def test_count_urls_none(self):
        self.assertEqual(count_urls("Hello, how are you?"), 0)
 
    def test_count_urls_http(self):
        self.assertEqual(count_urls("Visit http://example.com now"), 1)
 
    def test_count_urls_www(self):
        self.assertEqual(count_urls("Check www.example.com today"), 1)
 
    def test_count_urls_multiple(self):
        text = "See http://a.com and http://b.com"
        self.assertEqual(count_urls(text), 2)
 
    def test_count_urls_across_lines(self):
        """URLs on separate lines (as in a multi-line pasted email) should each be counted."""
        text = "Check this out:\nhttp://example.com/page\nand also\nhttp://example.com/other"
        self.assertEqual(count_urls(text), 2)
 
    def test_has_url_true(self):
        self.assertEqual(has_url("Click http://phish.com"), 1)
 
    def test_has_url_false(self):
        self.assertEqual(has_url("No links here"), 0)
 
    def test_count_urgent_keywords_specific_phrase(self):
        text = "Please verify your account and confirm your identity."
        self.assertEqual(count_urgent_keywords(text), 2)
 
    def test_count_urgent_keywords_ignores_generic_words(self):
        text = "Please respond immediately, this is urgent."
        self.assertEqual(count_urgent_keywords(text), 0)
 
    def test_count_urgent_keywords_none(self):
        text = "Let's grab coffee sometime."
        self.assertEqual(count_urgent_keywords(text), 0)
 
    def test_extract_features_combined(self):
        text = "Account suspended: click here http://fake.com to verify your account"
        result = extract_features(text)
        self.assertEqual(result["has_url"], 1)
        self.assertEqual(result["url_count"], 1)
        self.assertGreaterEqual(result["urgent_keyword_count"], 2)
        self.assertEqual(result["urgent_and_url"], 1)
 
    def test_urgent_and_url_requires_both(self):
        text = "Please verify your account at the front desk."
        result = extract_features(text)
        self.assertEqual(result["urgent_and_url"], 0)

        text2 = "Here's the report: http://example.com/report"
        result2 = extract_features(text2)
        self.assertEqual(result2["urgent_and_url"], 0)
 
 
    def test_extract_features_multiline_safe_email(self):
        """Mirrors a real multi-line safe email (course notice with links)."""
        email = """Dear Learners,
 
The lecture videos for Week 11 have been uploaded. Access them here:
https://onlinecourses.nptel.ac.in/course/unit?unit=111
 
Assignment 11 is also released here:
https://onlinecourses.nptel.ac.in/course/assignment?unit=111
 
Please submit before Wednesday, 23:59 IST.
 
Thanks and Regards,
NPTEL Team
 
To unsubscribe, send an email to unsubscribe@example.com."""
 
        result = extract_features(email)
        self.assertEqual(result["has_url"], 1)
        self.assertEqual(result["url_count"], 2)
        self.assertEqual(result["urgent_keyword_count"], 0)
        self.assertEqual(result["urgent_and_url"], 0)
 
    def test_extract_features_multiline_phishing_email(self):
        """A multi-line phishing email split across several lines."""
        email = """Dear Customer,
 
We noticed unusual login activity on your account.
Please verify your account immediately by clicking the link below:
 
http://fake-secure-bank.com/verify
 
If you do not verify your account within 24 hours,
it will be suspended.
 
Regards,
Security Team"""
 
        result = extract_features(email)
        self.assertEqual(result["has_url"], 1)
        self.assertGreaterEqual(result["url_count"], 1)
        self.assertGreaterEqual(result["urgent_keyword_count"], 2)
        self.assertEqual(result["urgent_and_url"], 1)
 
 
if __name__ == "__main__":
    unittest.main()
 
