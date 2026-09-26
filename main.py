import os
from train import main as train_model, MODEL_PATH, VECTORIZER_PATH
from predict import load_model, predict_email

def ensure_model_exists():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        print("NO trained model found - training now...\n")
        train_model()
        print()
    else:
        print("Loaded existing trained model.\n")

def read_multiline_email() -> str:
    print("Paste the email (can be multiple lines). Type END on its own line when done:")
    lines = []
    
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    return "\n".join(lines)

def run_interactive_loop(model, vectorizer, scaler):
    print("Phishing Email Detector")
    print("Paste an email's text and press Enter to classify it.")
    print("Type 'quit' to exit.\n")

    while True:
        first_line = input("> ").strip()

        if first_line.lower() == "quit":
            print("Goodbye..!!")
            break

        email_text = first_line + "\n" + read_multiline_email()

        if not email_text.strip():
            continue

        result = predict_email(email_text, model, vectorizer, scaler)
        print(f" -> {result['label']} (confidence: {result['confidence']})\n")

def main():
    ensure_model_exists()
    model, vectorizer, scaler = load_model()
    run_interactive_loop(model, vectorizer, scaler)

if __name__ == "__main__":
    main()
