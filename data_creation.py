import os
import numpy as np
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_exponential_growth(n_samples=200, growth_rate=0.02, noise_std=0.1, random_state=None):
    rng = np.random.RandomState(random_state)
    x = np.arange(n_samples)
    y = np.exp(growth_rate * x) + rng.normal(0, noise_std, size=n_samples)
    return pd.DataFrame({"x": x, "y": y})

def main():
    train_dir = os.path.join(BASE_DIR, "lab1", "train")
    test_dir = os.path.join(BASE_DIR, "lab1", "test")

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    train_datasets = [
        generate_exponential_growth(200, 0.02, 0.1, 0),
        generate_exponential_growth(250, 0.03, 0.15, 1),
        generate_exponential_growth(300, 0.025, 0.2, 2),
    ]

    test_datasets = [
        generate_exponential_growth(150, 0.02, 0.12, 10),
        generate_exponential_growth(180, 0.03, 0.18, 11),
    ]

    for i, df in enumerate(train_datasets, 1):
        path = os.path.join(train_dir, f"train_dataset_{i}.csv")
        df.to_csv(path, index=False)
        print(f"Saved {path} with shape {df.shape}")

    for i, df in enumerate(test_datasets, 1):
        path = os.path.join(test_dir, f"test_dataset_{i}.csv")
        df.to_csv(path, index=False)
        print(f"Saved {path} with shape {df.shape}")

if __name__ == "__main__":
    main()
