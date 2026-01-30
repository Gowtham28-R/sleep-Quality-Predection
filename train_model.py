import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load Data
print("Loading dataset...")
try:
    df = pd.read_csv('data/raw/Sleep_health.csv')
except FileNotFoundError:
    print("❌ Error: 'data/raw/Sleep_health.csv' not found.")
    exit()

# --- FIX: DROP PERSON ID ---
if 'Person ID' in df.columns:
    df = df.drop(columns=['Person ID'])
    print("⚠️ Dropped 'Person ID' column (Fix applied)")

# 2. Preprocessing
le_gender = LabelEncoder()
le_occupation = LabelEncoder()
le_bmi = LabelEncoder()
le_disorder = LabelEncoder()

# Fit encoders
df['Gender'] = le_gender.fit_transform(df['Gender'])
df['Occupation'] = le_occupation.fit_transform(df['Occupation'])
df['BMI Category'] = le_bmi.fit_transform(df['BMI Category'])
df['Sleep Disorder'] = le_disorder.fit_transform(df['Sleep Disorder'].fillna("None"))

# Handle Blood Pressure
if 'Blood Pressure' in df.columns:
    df[['Systolic', 'Diastolic']] = df['Blood Pressure'].str.split('/', expand=True).astype(int)
    df = df.drop(columns=['Blood Pressure'])

# Define Features (X) and Target (y)
X = df.drop(columns=['Quality of Sleep'])
y = df['Quality of Sleep']

# Categorize Target
def categorize_sleep(q):
    if q >= 8: return "Good"
    elif q >= 6: return "Average"
    else: return "Poor"

y_class = y.apply(categorize_sleep)

# 3. Train Model
print("Training Random Forest model...")
X_train, X_test, y_train, y_test = train_test_split(X, y_class, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4. Save Model & Encoders
artifacts = {
    'model': model,
    'le_gender': le_gender,
    'le_occupation': le_occupation,
    'le_bmi': le_bmi,
    'le_disorder': le_disorder
}

joblib.dump(artifacts, 'sleep_model_ml.pkl')
print("✅ Model trained and saved as 'sleep_model_ml.pkl'")