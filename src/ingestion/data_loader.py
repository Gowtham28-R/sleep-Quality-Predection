import pandas as pd
from pathlib import Path


class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def validate_file(self):
        if not self.filepath.exists():
            raise FileNotFoundError(f"Dataset not found: {self.filepath}")
        if self.filepath.suffix not in [".csv"]:
            raise ValueError("Only CSV files are supported")

    def load(self):
        self.validate_file()
        df = pd.read_csv(self.filepath)
        print("✅ Dataset loaded successfully")
        print("Shape:", df.shape)
        return df

    def basic_report(self, df):
        print("\n--- BASIC DATA REPORT ---")
        print(df.info())
        print("\nMissing values:\n", df.isnull().sum())
        print("\nStatistical summary:\n", df.describe(include="all"))


if __name__ == "__main__":
    loader = DataLoader("data/raw/sleep_health.csv")
    df = loader.load()
    loader.basic_report(df)
