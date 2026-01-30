from fastapi import FastAPI
from pydantic import BaseModel, Field
from src.inference.service import run_full_analysis

app = FastAPI(
    title="Sleep Quality Predictor API",
    description="AI-powered system to predict sleep quality and provide lifestyle recommendations",
    version="1.0.0"
)


# -------------------------
# Input Schema
# -------------------------
class SleepInput(BaseModel):
    gender: str = Field(example="Male")
    age: int = Field(example=28)
    occupation: str = Field(example="Software Engineer")
    sleep_duration: float = Field(example=6.5)
    physical_activity_level: int = Field(example=30)
    stress_level: int = Field(example=6)
    bmi_category: str = Field(example="Normal")
    heart_rate: int = Field(example=72)
    daily_steps: int = Field(example=6500)
    sleep_disorder: str = Field(example="None")
    systolic: int = Field(example=120)
    diastolic: int = Field(example=80)
    activity_stress_ratio: float = Field(example=4.2)
    cardio_load: float = Field(example=96.0)
    lifestyle_score: float = Field(example=30.5)


# -------------------------
# Routes
# -------------------------
@app.get("/")
def home():
    return {"status": "Sleep Quality Predictor API is running"}


@app.post("/predict")
def predict_sleep(data: SleepInput):
    result = run_full_analysis(data.dict())
    return result
