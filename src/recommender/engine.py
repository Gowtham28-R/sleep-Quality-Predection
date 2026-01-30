def generate_recommendations(user_input: dict, prediction: str):
    tips = []
    risk_factors = []

    # Sleep duration
    if user_input["sleep_duration"] < 6:
        tips.append("Try to increase your sleep duration to at least 7–8 hours.")
        risk_factors.append("Short sleep duration")

    # Physical activity
    if user_input["physical_activity_level"] < 30:
        tips.append("Increase your daily physical activity to improve sleep quality.")
        risk_factors.append("Low physical activity")

    # Stress
    if user_input["stress_level"] > 6:
        tips.append("Practice relaxation techniques such as meditation or deep breathing before sleep.")
        risk_factors.append("High stress level")

    # Heart health
    if user_input["heart_rate"] > 75:
        tips.append("High resting heart rate detected. Consider improving cardiovascular fitness.")
        risk_factors.append("Elevated heart rate")

    # Blood pressure
    if user_input["systolic"] > 130 or user_input["diastolic"] > 85:
        tips.append("Elevated blood pressure detected. Maintain a healthy diet and routine.")
        risk_factors.append("High blood pressure")

    # Sleep disorder
    if user_input["sleep_disorder"] != "None":
        tips.append("You may have a sleep disorder. Consider consulting a medical professional.")
        risk_factors.append("Sleep disorder indication")

    # Prediction-based advice
    if prediction == "Poor":
        tips.append("Your sleep quality is poor. Immediate lifestyle adjustments are recommended.")
    elif prediction == "Average":
        tips.append("Your sleep quality is average. Small improvements can significantly help.")
    else:
        tips.append("Your sleep quality is good. Maintain your current healthy routine.")

    return {
        "sleep_quality": prediction,
        "risk_factors": risk_factors,
        "recommendations": tips
    }
