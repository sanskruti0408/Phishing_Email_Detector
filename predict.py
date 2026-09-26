import joblib
from scipy.sparse import hstack, csr_matrix
import pandas as pd

from features import extract_features

MODEL_PATH = "phishing_model.joblib"
VECTORIZER_PATH = "vectorizer.joblib"
SCALER_PATH = "scaler.joblib"

def load_model():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, vectorizer, scaler

def predict_email(text: str, model, vectorizer, scaler) -> dict:
    tfidf_vec = vectorizer.transform([text])
    engineered = pd.DataFrame([extract_features(text)])
    engineered_scaled = scaler.transform(engineered.values)
    combined = hstack([tfidf_vec, csr_matrix(engineered_scaled)])

    prediction = model.predict(combined)[0]
    probability = model.predict_proba(combined)[0]

    label = "Phishing Email" if prediction == 1 else "Safe Email"
    confidence = probability[prediction]

    return {"label": label, "confidence": round(float(confidence), 4)}
