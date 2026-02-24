import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

def load_all_csv_from_folder(folder_path):
    dataframes = []
    filenames = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            full_path = os.path.join(folder_path, filename)
            df = pd.read_csv(full_path)
            dataframes.append(df)
            filenames.append(full_path)

    return dataframes, filenames

def save_preprocessed_data(dataframes, filenames, scaler=None):
    for df, path in zip(dataframes, filenames):
        transformed = scaler.transform(df)

        df_scaled = pd.DataFrame(transformed, columns=df.columns)

        df_scaled.to_csv(path, index=False)
        print(f" preprocessed file: {path}")

def main():
    train_path = "lab1/train"
    test_path = "lab1/test"

    train_dfs, train_files = load_all_csv_from_folder(train_path)
    test_dfs, test_files = load_all_csv_from_folder(test_path)

    full_train_data = pd.concat(train_dfs, ignore_index=True)

    scaler = StandardScaler()
    scaler.fit(full_train_data)

    save_preprocessed_data(train_dfs, train_files, scaler=scaler)

    save_preprocessed_data(test_dfs, test_files, scaler=scaler)

    print("Pred-obrabotka zaverchena")

if __name__ == "__main__":
    main()