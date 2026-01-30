import pandas as pd
from src.ingestion.data_loader import DataLoader
from src.preprocessing.cleaning import DataCleaner
from src.preprocessing.formatting import FeatureFormatter
from src.preprocessing.labels import label_sleep_quality


def run_preprocessing(input_path, output_path):
    loader = DataLoader(input_path)
    df = loader.load()

    cleaner = DataCleaner(df)
    df = cleaner.clean()

    formatter = FeatureFormatter(df)
    df = formatter.format()

    # Create new label
    df["sleep_quality_label"] = df["quality_of_sleep"].apply(label_sleep_quality)

    # Drop original numeric quality score
    df.drop(columns=["quality_of_sleep"], inplace=True)

    df.to_csv(output_path, index=False)
    print(f"\n✅ Clean dataset saved to: {output_path}")
    print("Final shape:", df.shape)
    print(df.head())


if __name__ == "__main__":
    run_preprocessing(
        input_path="data/raw/sleep_health.csv",
        output_path="data/processed/sleep_clean.csv"
    )
