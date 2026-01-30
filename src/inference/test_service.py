from src.inference.service import run_full_analysis

sample_input = {
    "gender": "Male",
    "age": 28,
    "occupation": "Software Engineer",
    "sleep_duration": 5.5,
    "physical_activity_level": 15,
    "stress_level": 8,
    "bmi_category": "Overweight",
    "heart_rate": 78,
    "daily_steps": 4000,
    "sleep_disorder": "Insomnia",
    "systolic": 138,
    "diastolic": 90,
    "activity_stress_ratio": 15 / (8 + 1),
    "cardio_load": (78 + 138) / 2,
    "lifestyle_score": 5.5 + 15 - 8
}

output = run_full_analysis(sample_input)

print("\n🧾 FULL SLEEP ANALYSIS RESULT:\n")
for k, v in output.items():
    print(k, ":", v)
