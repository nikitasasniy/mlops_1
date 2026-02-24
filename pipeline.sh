#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"

echo "Starting ML pipeline"

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate

pip install --upgrade pip --quiet
pip install -r req.txt --quiet

python data_creation.py
python data_preprocessing.py
python model_preparation.py
python model_testing.py

echo "Pipeline finished successfully"
