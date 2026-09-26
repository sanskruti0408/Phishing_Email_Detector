# 📧 Phishing Email Detector

A machine learning model built with Scikit-learn that classifies emails as **Phishing** or **Safe**, combining TF-IDF text analysis with engineered URL and keyword features — built as Task 3 of a Cyber Security Internship.

## 🎯 Project Objective

The goal is to build a working phishing-detection pipeline that goes beyond generic text classification by explicitly extracting and analyzing the kinds of signals real phishing emails tend to contain — suspicious URLs and urgency-driven language — rather than relying on word frequency alone.

## 🛡️ Features

- 📊 TF-IDF vectorization of email text
- 🔗 URL detection and counting (`has_url`, `url_count`)
- ⚠️ Targeted phishing-phrase detection (`urgent_keyword_count`)
- 🔀 Interaction feature (`urgent_and_url`) — flags urgency language only when paired with a URL, since urgency alone is common in legitimate emails too
- 🤖 Logistic Regression classifier (chosen over Naive Bayes — see Model Development Process below)
- 📈 Accuracy, classification report, and confusion matrix evaluation
- 🔮 Interactive CLI (`main.py`) for classifying real, multi-line pasted emails
- 🧪 14 automated unit tests, including real multi-line email cases

## 📊 Dataset

- **Phishing Validation Emails Dataset** (Zenodo, DOI: 10.5281/zenodo.13474746) — 2,000 labeled emails (1,000 Safe / 1,000 Phishing), CC-BY-4.0.
- **`data/extra_emails.csv`** — a supplemental, hand-curated set of 79 emails added during development to fix a diagnosed bias (see below): safe emails that legitimately contain URLs/deadlines (course notices, shipping updates, invoices), and additional varied phishing categories (business email compromise, tech support scams, fake refunds, romance scams, etc.). Oversampled 8x during training to give it sufficient statistical weight against the larger main dataset.

## 📁 Project Structure

```text
Phishing_Detector/
│
├── data/
│   ├── Phishing_validation_emails.csv
│   └── extra_emails.csv
├── features.py
├── train.py
├── predict.py
├── main.py
├── tests/
│   └── test_features.py
├── phishing_model.joblib
├── vectorizer.joblib
├── scaler.joblib
└── README.md
```

## ⚙️ Technologies Used

- Python
- Pandas
- Scikit-learn (`TfidfVectorizer`, `LogisticRegression`, `StandardScaler`, `train_test_split`, `metrics`)
- SciPy (sparse matrix operations)
- Joblib (model/vectorizer/scaler persistence)
- unittest

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install pandas scikit-learn joblib scipy
```

### 2. Run the detector

```bash
python main.py
```

On first run, this trains the model automatically (if no saved model is found), then opens an interactive prompt. Paste an email's text (multiple lines supported), type `END` on its own line, and press Enter to classify it. Type `quit` to exit.

## 🧪 Running Tests

```bash
python -m unittest discover -s tests -v
```

**Test Result**

Ran 14 tests in 0.004s

OK


All 14 automated tests passed successfully. ✅

## 📈 Results

**Test set performance:**

Accuracy: 1.0000
Confusion Matrix:
[[264 0]
[ 0 263]]


**Real-world verification** (fresh emails, not from the dataset):

| Email | Prediction | Confidence |
|---|---|---|
| A real NPTEL course notice with links and a deadline | Safe Email | 0.8256 |
| "Urgent: Verify your account immediately... Click here: http://fake-bank-alert.com" | Phishing Email | 1.0 |
| "Congratulations! You've won a $500 gift card. Claim your prize now: ..." | Phishing Email | 1.0 |
| "Your bank account has been flagged... Verify now at http://secure-bank-alert.com" | Phishing Email | 0.9096 |

## 🔧 Model Development Process

The first working version reached 100% test accuracy immediately — but real-world testing against an actual course notification email (containing links and a submission deadline) incorrectly flagged it as Phishing. Rather than accept the misleading 100% number, this was investigated and fixed:

1. **Diagnosed the cause** by inspecting the model's learned feature coefficients directly, rather than guessing. Found that a hand-crafted `urgent_keyword_count` feature had a disproportionately large coefficient, and that generic single words like "urgent," "immediately," and "verify" — common in legitimate transactional emails — were being counted as phishing signals.
2. **Removed generic single-word keywords**, keeping only specific multi-word phishing phrases (e.g. "account suspended," "verify your identity") that rarely appear in legitimate text.
3. **Added an interaction feature** (`urgent_and_url`) so urgency language only counts strongly when paired with a URL — matching the actual phishing pattern, rather than penalizing urgency language on its own.
4. **Switched from Multinomial Naive Bayes to Logistic Regression**, which handles mixed feature types (TF-IDF + engineered numeric features) more reliably, and **scaled the engineered features** with `StandardScaler` so they don't disproportionately dominate the TF-IDF features.
5. **Added targeted training examples** (safe emails with URLs, additional phishing categories) to fill a real gap in the original dataset.

This process is documented here deliberately — a perfect accuracy score straight out of the box is often a sign to investigate further, not a result to trust blindly.

## ⚠️ Known Limitations

- This model analyzes plain email **text only**. It does not inspect raw HTML source, so it cannot detect display-text/href mismatches (e.g. a button labeled "Verify Account" that actually links to a different domain) — a technique real phishing emails commonly use and that security professionals check via "View Original"/"Show Original" in email clients.
- It does not check sender authentication (SPF/DKIM/DMARC), which is a standard part of real-world phishing detection.
- It detects phishing *intent*, not general spam. A legitimate marketing email landing in a spam folder (due to bulk-sending patterns) is a different problem from credential-phishing, and this model correctly distinguishes the two.

## 🔒 Ethical Use

This project is intended for educational and defensive cybersecurity purposes — understanding how phishing-detection systems can be built, not for crafting phishing content.

## 🎓 Internship Project

- **Project:** Phishing Email Detection Model
- **Domain:** Cyber Security & Ethical Hacking
- **Role:** Cyber Security Intern

This project was developed as part of a cybersecurity internship to demonstrate practical understanding of applying machine learning to a real security problem, including feature engineering, proper train/test methodology, root-cause debugging, and honest evaluation.

## 👩‍💻 Author

**Sanskruti Vharamble**

Diploma in Computer Engineering<br>
Cyber Security & Ethical Hacking
