"""
main.py — FitMind AI FastAPI Server
=====================================
Start with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from ml_engine import get_engine

app = FastAPI(title="FitMind AI API", version="1.0.0")

# ── CORS — allow React dev server ─────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Request / Response schemas ────────────────────────────────
class UserProfile(BaseModel):
    name:             str            = Field(..., min_length=1)
    age:              float          = Field(..., ge=10, le=100)
    gender:           str            = Field(..., pattern="^(Male|Female|Other)$")
    height:           float          = Field(..., ge=100, le=250)
    weight:           float          = Field(..., ge=30, le=250)
    targetWeight:     Optional[float] = None
    diets:            List[str]      = []
    goal:             str
    activity:         str
    allergies:        Optional[str]  = ""
    medical:          Optional[str]  = ""
    sleep:            Optional[str]  = "7–8"
    water:            Optional[str]  = ""
    workoutDuration:  Optional[str]  = ""


class MacroInfo(BaseModel):
    protein: int
    carbs:   int
    fats:    int


class MealItem(BaseModel):
    time:        str
    name:        str
    description: str


class ExerciseItem(BaseModel):
    name: str
    sets: str
    tip:  str


class DaySchedule(BaseModel):
    day:   str
    focus: str
    type:  str


class PlanResponse(BaseModel):
    name:             str
    age:              float
    gender:           str
    height:           float
    weight:           float
    targetWeight:     Optional[float]
    bmi:              float
    bmr:              int
    tdee:             int
    goal:             str
    activity:         str
    diet:             str
    greeting:         str
    bmiInsight:       str
    targetCalories:   int
    dietCategory:     str
    exerciseCategory: str
    macros:           MacroInfo
    meals:            List[MealItem]
    exercises:        List[ExerciseItem]
    weeklySchedule:   List[DaySchedule]
    tips:             List[str]
    waterTarget:      str
    sleepAdvice:      str


# ── Routes ────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "FitMind AI API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PlanResponse)
def predict(profile: UserProfile):
    try:
        engine = get_engine()
        result = engine.predict(profile.model_dump())

        diet_str = ", ".join(profile.diets) if profile.diets else "No preference"

        return PlanResponse(
            name=profile.name,
            age=profile.age,
            gender=profile.gender,
            height=profile.height,
            weight=profile.weight,
            targetWeight=profile.targetWeight,
            bmi=result["bmi"],
            bmr=result["bmr"],
            tdee=result["tdee"],
            goal=profile.goal,
            activity=profile.activity,
            diet=diet_str,
            greeting=result["greeting"],
            bmiInsight=result["bmiInsight"],
            targetCalories=result["targetCalories"],
            dietCategory=result["dietCategory"],
            exerciseCategory=result["exerciseCategory"],
            macros=MacroInfo(**result["macros"]),
            meals=[MealItem(**m) for m in result["meals"]],
            exercises=[ExerciseItem(**e) for e in result["exercises"]],
            weeklySchedule=[DaySchedule(**d) for d in result["weeklySchedule"]],
            tips=result["tips"],
            waterTarget=result["waterTarget"],
            sleepAdvice=result["sleepAdvice"],
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="ML models not found. Please run: python train_model.py"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
