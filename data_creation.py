import os
import numpy as np
import pandas as pd

def generate_exponential_growth(n_samples=200, growth_rate=0.02, noise_std=0.1, random_state=None):
    rng = np.random.RandomState(random_state)
    x = np.arange(n_samples)
    y = np.exp(growth_rate * x) + rng.normal(0, noise_std, size=n_samples)
    return pd.DataFrame({"x": x, "y": y})

def main():
    os.makedirs("lab1/train", exist_ok=True)
    os.makedirs("lab1/test", exist_ok=True)

    train_datasets = [
        generate_exponential_growth(n_samples=200, growth_rate=0.02, noise_std=0.1, random_state=0),
        generate_exponential_growth(n_samples=250, growth_rate=0.03, noise_std=0.15, random_state=1),
        generate_exponential_growth(n_samples=300, growth_rate=0.025, noise_std=0.2, random_state=2),
    ]

    test_datasets = [
        generate_exponential_growth(n_samples=150, growth_rate=0.02, noise_std=0.12, random_state=10),
        generate_exponential_growth(n_samples=180, growth_rate=0.03, noise_std=0.18, random_state=11),
    ]

    for i, df in enumerate(train_datasets, start=1):
        path = f"lab1/train/train_dataset_{i}.csv"
        df.to_csv(path, index=False)
        print(f"Saved {path} with shape {df.shape}")

    for i, df in enumerate(test_datasets, start=1):
        path = f"lab1/test/test_dataset_{i}.csv"
        df.to_csv(path, index=False)
        print(f"Saved {path} with shape {df.shape}")

if __name__ == "__main__":
    main()