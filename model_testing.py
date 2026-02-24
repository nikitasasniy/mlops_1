import os
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import root_mean_squared_error

def load_all_csv_from_folder(folder_path):
    dataframes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder_path, filename)
            df = pd.read_csv(full_path)
            dataframes.append(df)
    return dataframes

def main():
    test_path = "lab1/test"

    test_dfs = load_all_csv_from_folder(test_path)
    full_test = pd.concat(test_dfs, ignore_index=True)

    X_test = full_test[["x"]].values
    y_test = full_test["y"].values

    with open("lab1/model.pkl", "rb") as f:
        model = pickle.load(f)

    y_pred = model.predict(X_test)

    rmse = root_mean_squared_error(y_test, y_pred)

    print(f"RMSE is: {rmse:.4f}")

if __name__ == "__main__":
    main()