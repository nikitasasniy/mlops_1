import pytest
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def clean_text(text):
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

@pytest.fixture(scope="module")
def model_and_vectorizer():
    model_path = "models/sentiment_model.pkl"
    vectorizer_path = "models/vectorizer.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        pytest.fail("Run 'python train_model.py' first")
    
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

@pytest.fixture(scope="module")
def test_data():
    data_path = "data/sample_data.csv"
    if not os.path.exists(data_path):
        pytest.fail(f"Test data not found at {data_path}")
    return pd.read_csv(data_path)

def test_model_accuracy(model_and_vectorizer, test_data):
    model, vectorizer = model_and_vectorizer
    df = test_data
    
    X_test = vectorizer.transform(df['text'].apply(clean_text))
    y_true = df['label']
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_true, y_pred)
    assert accuracy > 0.90, f"Accuracy too low: {accuracy:.4f}"

def test_model_exists():
    assert os.path.exists("models/sentiment_model.pkl")

def test_vectorizer_exists():
    assert os.path.exists("models/vectorizer.pkl")

def test_data_exists():
    assert os.path.exists("data/sample_data.csv")
    