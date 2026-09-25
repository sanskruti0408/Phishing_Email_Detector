import pandas as pd
import joblib
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from features import extract_features

DATA_PATH = "data/Phishing_validation_emails.csv"
MODEL_PATH = "phishing_model.joblib"
VECTORIZER_PATH = "vectorizer.joblib"

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["label"] = df["Email Type"].map({"Phishing Email": 1, "Safe Email": 0})
    return df

def build_features(texts: pd.Series, vectorizer: TfidfVectorizer, fit: bool = False):
    if fit:
        tfidf_matrix = vectorizer.fit_transform(texts)
    else:
        tfidf_matrix = vectorizer.transform(texts)

    engineered = pd.DataFrame([extract_features(t) for t in texts])
    engineered_sparse = csr_matrix(engineered.values)

    combined = hstack([tfidf_matrix, engineered_sparse])
    return combined

def main():
    df = load_data(DATA_PATH)
    X_text = df["Email Text"]
    y = df["label"]

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X_text, y, test_size=0.2, random_state=42, stratify=y )

    vectorizer = TfidfVectorizer(stop_words = "english", max_features = 3000)

    X_train = build_features(X_train_text, vectorizer, fit=True)
    X_test = build_features(X_test_text, vectorizer, fit=False)

    model = MultinomialNB()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Safe Email", "Phishing Email"]))

    print("Confustion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    print("(rows = actual, columns = predicted; order = [Safe, Phishing])")

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"\nModel saved to {MODEL_PATH}")
    print(f"Vectorizer savedbto {VECTORIZER_PATH}")

if __name__ == "__main__":
    main()


    

    
