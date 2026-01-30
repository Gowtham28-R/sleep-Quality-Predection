import joblib
import pandas as pd
import numpy as np
from pathlib import Path

MODEL_PATH = Path("models/sleep_model.pkl")
PIPELINE_PATH = Path("models/feature_pipeline.pkl")


class SleepPredictor:
    def __init__(self):
        if not MODEL_PATH.exists() or not PIPELINE_PATH.exists():
            raise FileNotFoundError("Model or feature pipeline not found. Train model first.")

        self.model = joblib.load(MODEL_PATH)
        self.pipeline = joblib.load(PIPELINE_PATH)

    def preprocess(self, input_dict: dict):
        df = pd.DataFrame([input_dict])
        return self.pipeline.transform(df)

    def predict(self, input_dict: dict):
        X = self.preprocess(input_dict)

        prediction = self.model.predict(X)[0]
        probability = np.max(self.model.predict_proba(X))

        return {
            "prediction": str(prediction),
            "confidence": round(float(probability), 3)
        }
