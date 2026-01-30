import pandas as pd
from src.config.features import TARGET
from src.features.engineer import add_engineered_features
from src.features.transformer import build_transformer, save_transformer


def run_feature_pipeline(input_path):
    df = pd.read_csv(input_path)

    df = add_engineered_features(df)

    X = df.drop(columns=[TARGET])
    y = df[TARGET]

    transformer = build_transformer()
    X_transformed = transformer.fit_transform(X)

    save_transformer(transformer)

    print("✅ Feature pipeline built")
    print("Final feature matrix shape:", X_transformed.shape)

    return X_transformed, y


if __name__ == "__main__":
    run_feature_pipeline("data/processed/sleep_clean.csv")
