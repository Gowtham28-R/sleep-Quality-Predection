from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib
import pandas as pd
import numpy as np

app = FastAPI()

# --- Load Trained ML Model ---
try:
    artifacts = joblib.load('sleep_model_ml.pkl')
    model = artifacts['model']
    le_gender = artifacts['le_gender']
    le_occupation = artifacts['le_occupation']
    le_bmi = artifacts['le_bmi']
    le_disorder = artifacts['le_disorder']
    print("✅ ML Model Loaded Successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print("Run 'python train_model.py' first!")
    exit()

class SleepInput(BaseModel):
    age: int
    gender: str
    occupation: str
    sleep_duration: float
    bedtime_hour: int
    physical_activity: int
    stress_level: int
    bmi_category: str
    heart_rate: int
    daily_steps: int
    sleep_disorder: str
    blood_pressure_systolic: int = 120
    blood_pressure_diastolic: int = 80

@app.post("/predict")
def predict_hybrid(data: SleepInput):
    # 1. Helper to safely transform inputs
    def safe_transform(le, value):
        if value in le.classes_:
            return le.transform([value])[0]
        else:
            return le.transform([le.classes_[0]])[0]

    # 2. Prepare Features for ML
    gender_enc = safe_transform(le_gender, data.gender)
    occ_enc = safe_transform(le_occupation, data.occupation) 
    bmi_enc = safe_transform(le_bmi, data.bmi_category)
    disorder_enc = safe_transform(le_disorder, data.sleep_disorder)

    features = pd.DataFrame([{
        'Gender': gender_enc,
        'Age': data.age,
        'Occupation': occ_enc,
        'Sleep Duration': data.sleep_duration,
        'Physical Activity Level': data.physical_activity,
        'Stress Level': data.stress_level,
        'BMI Category': bmi_enc,
        'Heart Rate': data.heart_rate,
        'Daily Steps': data.daily_steps,
        'Sleep Disorder': disorder_enc,
        'Systolic': data.blood_pressure_systolic,
        'Diastolic': data.blood_pressure_diastolic
    }])

    # 3. ML Prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    confidence = float(max(probabilities) * 100)
    
    # Map ML result to a Base Score
    score_map = {"Good": 90, "Average": 65, "Poor": 40}
    score = score_map.get(prediction, 50)
    
    # Adjust score based on confidence
    if prediction == "Good": score += (confidence - 50) / 5
    elif prediction == "Poor": score -= (confidence - 50) / 5

    # --- 4. CLINICAL SAFETY LAYER (The Fix) ---
    # Force 'Poor' if sleep is critically low, overriding ML if necessary.
    recommendations = []
    
    if data.sleep_duration < 5.0:
        prediction = "Poor"
        score = min(score, 45) # Force score drop
        recommendations.append("🚨 **Critical Sleep Debt:** < 5 hours is clinically insufficient.")
    
    if data.stress_level > 8:
        score -= 10
        recommendations.append("🧠 **High Cortisol:** Stress is severely impacting sleep quality.")

    # Clamp Score
    score = min(100, max(0, int(score)))

    # 5. Chronotype Logic
    if data.bedtime_hour >= 23 or data.bedtime_hour < 3:
        chronotype = "Wolf (Night Owl)"
    elif data.bedtime_hour < 22:
        chronotype = "Lion (Early Bird)"
    else:
        chronotype = "Bear (Normal)"

    # 6. Generate Response
    if not recommendations:
        if prediction == "Good": recommendations.append("✅ **Optimal:** Your biometrics are excellent.")
        elif prediction == "Poor": recommendations.append("⚠️ **Pattern:** Biometrics match poor sleep profiles.")
        else: recommendations.append("ℹ️ **Stable:** Routine is average. Try increasing activity.")

    return {
        "score": score,
        "label": prediction,
        "chronotype": chronotype,
        "breakdown": {
            "Sleep Hygiene": int(min(data.sleep_duration * 10, 40)) if data.sleep_duration > 4 else 10,
            "Recovery": int(100 - data.heart_rate + (data.daily_steps/200)),
            "Mental State": int(100 - (data.stress_level * 10))
        },
        "recommendations": recommendations
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)