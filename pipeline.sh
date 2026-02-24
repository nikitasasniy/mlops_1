#!/bin/bashbash


set -e

echo " Installing dependencies"
echo " "
pip install numpy pandas scikit-learn --quiet
echo " "
echo "Running data creation file"
echo " "
python3 lab1/data_creation.py
echo " "
echo "Running data preprocessing file"
echo " "
python3 lab1/data_preprocessing.py
echo " "
echo "Running model preparation file"
echo " "
python3 lab1/model_preparation.py
echo " "
echo "Running model testing file"
echo " "
python3 lab1/model_testing.py