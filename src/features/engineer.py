def add_engineered_features(df):
    df["activity_stress_ratio"] = df["physical_activity_level"] / (df["stress_level"] + 1)
    df["cardio_load"] = (df["heart_rate"] + df["systolic"]) / 2
    df["lifestyle_score"] = (
        df["sleep_duration"] +
        df["physical_activity_level"] -
        df["stress_level"]
    )
    return df
