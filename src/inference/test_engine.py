from src.inference.engine import SleepPredictor

sample_input = {
    "gender": "Male",
    "age": 28,
    "occupation": "Software Engineer",
    "sleep_duration": 6.2,
    "physical_activity_level": 40,
    "stress_level": 7,
    "bmi_category": "Normal",
    "heart_rate": 72,
    "daily_steps": 6000,
    "sleep_disorder": "None",
    "systolic": 125,
    "diastolic": 80,
    "activity_stress_ratio": 40 / (7 + 1),
    "cardio_load": (72 + 125) / 2,
    "lifestyle_score": 6.2 + 40 - 7
}

engine = SleepPredictor()
result = engine.predict(sample_input)

print("\n🧠 Prediction Result:")
print(result)
