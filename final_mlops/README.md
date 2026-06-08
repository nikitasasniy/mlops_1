# Final MLOps Project - Sentiment Analysis API

This project is a sentiment analysis API (Positive/Negative) built with FastAPI and scikit-learn. It is the final project for the MLOps course.

---

## Features

- FastAPI REST API
- Logistic Regression model with TF-IDF vectorizer
- Dataset with 20 sentences (10 positive, 10 negative)
- Training script `train_model.py`
- pytest tests (module tests + quality tests)
- Docker containerization (Dockerfile + docker-compose)
- Jenkins CI/CD pipeline (`Jenkinsfile`)
- DVC for dataset versioning
- DVC remote storage

final_mlops/
├── app/
│ └── main.py
├── models/
│ ├── sentiment_model.pkl
│ └── vectorizer.pkl
├── tests/
│ └── test_model.py
├── data/
│ └── sample_data.csv
├── train_model.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── dvc.yaml
└── .gitignore


## How to Run

### Option 1: Docker

```bash
cd final_mlops
docker-compose up -d


### Option 2: Without Docker

cd final_mlops
pip install -r requirements.txt
python train_model.py
uvicorn app.main:app --host 0.0.0.0 --port 8000


## Run Tests

python -m pytest tests/ -v


Jenkins Pipeline

Stages defined in Jenkinsfile:

    Checkout – Pull code from GitHub

    Setup Environment – Create venv and install dependencies

    Train Model – Run training script

    Run Tests – Execute pytest

    Docker Build & Push – Build Docker image and push to Docker Hub


##  Dataset is versioned with DVC:
dvc add data/sample_data.csv
dvc push


## Requirements :
fastapi
uvicorn
scikit-learn==1.7.2
pandas
joblib
pytest
python-multipart


##  Retrain Model

python train_model.py
python -m pytest tests/ -v
docker-compose up -d --build


Docker Hub: asghossein/sentiment-final:latest

