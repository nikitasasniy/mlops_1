import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

def load_all_csv_from_folder(folder_path):
    dataframes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder_path, filename)
            df = pd.read_csv(full_path)
            dataframes.append(df)
    return dataframes

def main():
    train_path = "lab1/train"

    train_dfs = load_all_csv_from_folder(train_path)

    full_train = pd.concat(train_dfs, ignore_index=True)

    X = full_train[["x"]].values
    y = full_train["y"].values

    model = LinearRegression()
    model.fit(X, y)

    with open("lab1/model.pkl", "wb") as f:
        pickle.dump(model, f)

    print("Model trained and saved to lab1/model.pkl")
    print(f"Model coefficient: {model.coef_[0]:.4f}, intercept: {model.intercept_:.4f}")

if __name__ == "__main__":
    main()