from src.inference.engine import SleepPredictor
from src.recommender.engine import generate_recommendations

predictor = SleepPredictor()

def run_full_analysis(user_input: dict):
    result = predictor.predict(user_input)
    advice = generate_recommendations(user_input, result["prediction"])

    return {
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "risk_factors": advice["risk_factors"],
        "recommendations": advice["recommendations"]
    }
