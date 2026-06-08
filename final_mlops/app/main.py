from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import joblib
import os
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

model = None
vectorizer = None

MODEL_PATH = "models/sentiment_model.pkl"
VECTORIZER_PATH = "models/vectorizer.pkl"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, vectorizer
    logger.info(f"Loading model from {MODEL_PATH}")
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            model = None
            vectorizer = None
    else:
        logger.error("Model files not found")
    yield
    logger.info("Shutting down")

app = FastAPI(title="Final MLOps Sentiment API", lifespan=lifespan)

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

class TextInput(BaseModel):
    text: str

class SentimentOutput(BaseModel):
    sentiment: str
    score: float

@app.get("/")
def root():
    return {"message": "Sentiment Analysis API", "status": "running"}

@app.post("/predict", response_model=SentimentOutput)
def predict_sentiment(input_data: TextInput):
    if model is None or vectorizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    text_clean = clean_text(input_data.text)
    X_input = vectorizer.transform([text_clean])
    prediction = model.predict(X_input)[0]
    proba = model.predict_proba(X_input)[0]
    
    sentiment = "POSITIVE" if prediction == 1 else "NEGATIVE"
    score = float(max(proba))
    
    return SentimentOutput(sentiment=sentiment, score=score)

@app.get("/health")
def health():
    return {"status": "healthy" if model is not None else "unhealthy", "model_loaded": model is not None}
