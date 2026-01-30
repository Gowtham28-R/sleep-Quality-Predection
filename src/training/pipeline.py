import pandas as pd
from src.features.pipeline import run_feature_pipeline
from src.training.trainer import train_and_select


def run_training():
    X, y = run_feature_pipeline("data/processed/sleep_clean.csv")
    train_and_select(X, y)


if __name__ == "__main__":
    run_training()
