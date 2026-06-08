import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def main():
    data_path = "data/sample_data.csv"
    models_dir = "models"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"Dataset loaded with {len(df)} samples.")
    
    df['clean_text'] = df['text'].apply(clean_text)
    
    X = df['clean_text']
    y = df['label']
    
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X_features = vectorizer.fit_transform(X)
    
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_features, y)
    
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(model, os.path.join(models_dir, "sentiment_model.pkl"))
    joblib.dump(vectorizer, os.path.join(models_dir, "vectorizer.pkl"))
    
    print("Model and vectorizer saved successfully")

if __name__ == "__main__":
    main()