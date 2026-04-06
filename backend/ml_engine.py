"""
ml_engine.py — FitMind AI ML Recommendation Engine
====================================================
Loads trained models and produces structured diet + exercise plans.
"""

import joblib
import json
import numpy as np
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"

# ── Exercise database keyed by exercise_category ──────────────
EXERCISE_DB = {
    0: {  # Cardio Focus
        "Weight Loss": [
            {"name": "Brisk Walking / Jogging",   "sets": "30–45 min continuous",   "tip": "Maintain 60–70% max heart rate for fat burn zone"},
            {"name": "Cycling (stationary/road)",  "sets": "30 min, 3×/week",        "tip": "Keeps joints safe while burning calories effectively"},
            {"name": "Jump Rope",                  "sets": "3 × 5 min intervals",    "tip": "Burns ~10 kcal/min — one of the most efficient cardio exercises"},
            {"name": "Swimming",                   "sets": "20–30 min, 3×/week",     "tip": "Full-body, zero-impact — excellent for beginners"},
            {"name": "Elliptical Trainer",         "sets": "30 min moderate pace",   "tip": "Low impact but high calorie burn, great for knees"},
            {"name": "Stair Climbing",             "sets": "3 × 10 min",             "tip": "Works glutes and quads hard — burns more than flat walking"},
        ],
        "Weight Gain": [
            {"name": "Light Cycling",    "sets": "20 min easy pace",  "tip": "Maintain cardiovascular health without burning excess calories"},
            {"name": "Walking",          "sets": "30 min daily",       "tip": "Active recovery — keeps metabolism healthy during bulk"},
            {"name": "Swimming (easy)",  "sets": "20 min, 2×/week",   "tip": "Builds appetite and aids recovery between strength sessions"},
        ],
    },
    1: {  # Strength — Beginner
        "Weight Loss": [
            {"name": "Bodyweight Squats",    "sets": "3 × 15 reps", "tip": "Builds leg muscle which raises resting metabolism"},
            {"name": "Push-Ups",             "sets": "3 × 10 reps", "tip": "Modify on knees if needed — focus on full range"},
            {"name": "Dumbbell Rows",        "sets": "3 × 12 reps", "tip": "Squeeze shoulder blades together at the top"},
            {"name": "Plank",                "sets": "3 × 30 sec",  "tip": "Keep hips level — don't let them sag or rise"},
            {"name": "Glute Bridges",        "sets": "3 × 15 reps", "tip": "Squeeze glutes at top — protects lower back"},
            {"name": "Dumbbell Shoulder Press", "sets": "3 × 10 reps", "tip": "Start light and focus on controlled descent"},
        ],
        "Weight Gain": [
            {"name": "Goblet Squats",        "sets": "4 × 12 reps", "tip": "Hold dumbbell at chest — great for beginners to learn squat"},
            {"name": "Dumbbell Bench Press", "sets": "4 × 10 reps", "tip": "Full range of motion, keep feet flat on floor"},
            {"name": "Seated Cable Row",     "sets": "3 × 12 reps", "tip": "Pull to navel, control the return"},
            {"name": "Dumbbell Lunges",      "sets": "3 × 12 each", "tip": "Keep front knee over ankle — not past toes"},
            {"name": "Lat Pulldown",         "sets": "3 × 12 reps", "tip": "Pull to upper chest, lean slightly back"},
            {"name": "Dumbbell Bicep Curl",  "sets": "3 × 12 reps", "tip": "Keep elbows pinned to your sides"},
        ],
        "Muscle Gain": [
            {"name": "Barbell Back Squat",   "sets": "4 × 8 reps",  "tip": "Break parallel, brace core throughout"},
            {"name": "Dumbbell Bench Press", "sets": "4 × 10 reps", "tip": "Full ROM — touch chest, lock out at top"},
            {"name": "Barbell Row",          "sets": "4 × 8 reps",  "tip": "Hinge at hips, pull bar to lower chest"},
            {"name": "Overhead Press",       "sets": "3 × 10 reps", "tip": "Squeeze glutes and brace abs for stability"},
            {"name": "Romanian Deadlift",    "sets": "3 × 10 reps", "tip": "Feel hamstring stretch before returning up"},
            {"name": "Pull-Ups / Lat PD",    "sets": "3 × 8 reps",  "tip": "Full hang at bottom, chin over bar at top"},
        ],
        "Body Building": [
            {"name": "Barbell Squat",         "sets": "4 × 10 reps", "tip": "Control descent — 3 sec down, explode up"},
            {"name": "Incline Bench Press",   "sets": "4 × 10 reps", "tip": "Targets upper chest for full pec development"},
            {"name": "Deadlift",              "sets": "4 × 6 reps",  "tip": "Hips and shoulders rise together from floor"},
            {"name": "Barbell Curl",          "sets": "3 × 12 reps", "tip": "Supinate wrists at top for peak contraction"},
            {"name": "Tricep Pushdown",       "sets": "3 × 15 reps", "tip": "Lock elbows at sides, full extension at bottom"},
            {"name": "Lateral Raises",        "sets": "4 × 15 reps", "tip": "Lead with elbows, stop at shoulder height"},
        ],
    },
    2: {  # Strength — Advanced
        "Weight Loss": [
            {"name": "Barbell Back Squat",    "sets": "5 × 5 reps",  "tip": "Heavy compound movement — torches calories post-workout"},
            {"name": "Deadlift",              "sets": "4 × 5 reps",  "tip": "Greatest hormonal response of any exercise"},
            {"name": "Barbell Bench Press",   "sets": "4 × 6 reps",  "tip": "Progressive overload — add 2.5kg when you hit top reps"},
            {"name": "Pull-Ups (weighted)",   "sets": "4 × 6 reps",  "tip": "Add a dip belt when bodyweight becomes easy"},
            {"name": "Clean & Press",         "sets": "3 × 5 reps",  "tip": "Full-body explosive movement — high metabolic demand"},
            {"name": "Farmers Carry",         "sets": "4 × 40m",     "tip": "Heavy load, controlled stride, builds functional strength"},
        ],
        "Muscle Gain": [
            {"name": "Barbell Squat (heavy)", "sets": "5 × 5 reps",  "tip": "3–5 min rest between sets — true strength work"},
            {"name": "Romanian Deadlift",     "sets": "4 × 8 reps",  "tip": "Loaded stretch — key for hamstring hypertrophy"},
            {"name": "Weighted Pull-Ups",     "sets": "4 × 6 reps",  "tip": "Best lat exercise — beats lat pulldown for growth"},
            {"name": "Incline Barbell Press", "sets": "4 × 8 reps",  "tip": "Upper chest is often underdeveloped — prioritize this"},
            {"name": "Cable Fly",             "sets": "3 × 15 reps", "tip": "Maintain constant tension — squeeze hard at center"},
            {"name": "Hack Squat",            "sets": "3 × 12 reps", "tip": "Great quad isolator for leg development"},
        ],
        "Body Building": [
            {"name": "Barbell Squat",         "sets": "5 × 6 reps",  "tip": "Control the negative — 2-3 sec down"},
            {"name": "Deadlift",              "sets": "4 × 5 reps",  "tip": "Alternate sumo and conventional to hit different muscles"},
            {"name": "Weighted Dips",         "sets": "4 × 8 reps",  "tip": "Forward lean = more chest, upright = more triceps"},
            {"name": "T-Bar Row",             "sets": "4 × 10 reps", "tip": "Chest supported version removes low-back fatigue"},
            {"name": "Standing Barbell Curl", "sets": "4 × 10 reps", "tip": "Strict form — no swinging"},
            {"name": "Skull Crushers",        "sets": "4 × 12 reps", "tip": "Lower bar to forehead, extend fully at top"},
        ],
    },
    3: {  # HIIT
        "Weight Loss": [
            {"name": "Burpees",              "sets": "4 × 10 reps",      "tip": "Best HIIT movement — full body, zero equipment"},
            {"name": "Treadmill Sprints",    "sets": "8 × 30 sec on/off", "tip": "Sprint at 80–90% max effort, walk to recover"},
            {"name": "Box Jumps",            "sets": "4 × 8 reps",       "tip": "Land softly on full foot — protect knees"},
            {"name": "Mountain Climbers",    "sets": "4 × 30 sec",       "tip": "Drive knees explosively — keep hips level"},
            {"name": "Kettlebell Swings",    "sets": "4 × 15 reps",      "tip": "Hip hinge — not a squat — power from glutes"},
            {"name": "Battle Ropes",         "sets": "4 × 20 sec",       "tip": "Alternate arms, maintain low squat position"},
        ],
        "Muscle Gain": [
            {"name": "Plyometric Push-Ups",  "sets": "4 × 8 reps",  "tip": "Explosive push — builds fast-twitch muscle fiber"},
            {"name": "Jump Squats",          "sets": "4 × 10 reps", "tip": "Land in squat position — full depth each rep"},
            {"name": "Medicine Ball Slams",  "sets": "4 × 12 reps", "tip": "Full body extension — great core driver"},
            {"name": "Sprint Intervals",     "sets": "6 × 30 sec",  "tip": "Max effort sprints build leg power and mass"},
            {"name": "Kettlebell Clean",     "sets": "3 × 8 each",  "tip": "Keep bell close to body on the way up"},
            {"name": "Sled Push",            "sets": "4 × 20m",     "tip": "Drive through your quads — one of the best leg builders"},
        ],
    },
    4: {  # Yoga / Mobility
        "Weight Loss": [
            {"name": "Sun Salutation Flow",  "sets": "5 rounds daily",   "tip": "Builds heat and flexibility — great morning ritual"},
            {"name": "Warrior Sequence",     "sets": "3 × 5 min hold",   "tip": "Strengthens legs and core while building flexibility"},
            {"name": "Vinyasa Flow",         "sets": "20–30 min",        "tip": "Moving meditation — burns calories and reduces cortisol"},
            {"name": "Pigeon Pose",          "sets": "3 × 60 sec each",  "tip": "Opens hips — crucial for anyone with desk job"},
            {"name": "Core Yoga Circuit",    "sets": "3 × 10 min",       "tip": "Boat pose, plank flows, and leg lifts build deep core"},
            {"name": "Yin Yoga",             "sets": "30 min evening",   "tip": "Held poses reduce stress — cortisol reduction aids fat loss"},
        ],
        "Weight Gain": [
            {"name": "Restorative Yoga",     "sets": "20 min daily",     "tip": "Active recovery — improves muscle repair between sessions"},
            {"name": "Dynamic Stretching",   "sets": "10 min pre-lift",  "tip": "Increases range of motion for heavier training"},
            {"name": "Foam Rolling",         "sets": "10 min daily",     "tip": "Breaks up fascia — allows muscles to grow more freely"},
        ],
    },
}

# ── Meal plan database keyed by diet_category ──────────────────
MEAL_DB = {
    0: {  # Balanced — vegetarian by default
        "meals": [
            {"time": "Breakfast (7–8 AM)",     "name": "Oats & Fruits",            "description": "1 cup oats with banana, apple slices, honey and a glass of milk"},
            {"time": "Mid-Morning (10–11 AM)", "name": "Fruit & Nuts",             "description": "1 apple + handful of mixed nuts (20g) + green tea"},
            {"time": "Lunch (1–2 PM)",         "name": "Rice & Dal",               "description": "1.5 cups rice, 1 cup dal, mixed vegetable sabzi, salad"},
            {"time": "Pre-Workout (4–5 PM)",   "name": "Banana & Peanut Butter",   "description": "1 banana + 1 tbsp peanut butter + 1 glass milk"},
            {"time": "Dinner (7–8 PM)",        "name": "Roti & Paneer Sabzi",      "description": "3 whole wheat rotis, 1 cup paneer curry, steamed vegetables"},
        ]
    },
    1: {  # High Protein
        "meals": [
            {"time": "Breakfast (7–8 AM)",     "name": "Egg White Omelette",       "description": "6 egg whites + 2 yolks, spinach, cheese — 40g protein"},
            {"time": "Mid-Morning (10–11 AM)", "name": "Protein Shake",             "description": "1 scoop whey + 250ml milk + 1 banana — 35g protein"},
            {"time": "Lunch (1–2 PM)",         "name": "Paneer Rice Bowl",          "description": "200g paneer, 1.5 cups rice, broccoli, olive oil — high protein veg"},
            {"time": "Pre-Workout (4–5 PM)",   "name": "Greek Yogurt & Almonds",    "description": "200g Greek yogurt + 20 almonds — 25g protein"},
            {"time": "Dinner (7–8 PM)",        "name": "Paneer / Tofu Stir Fry",      "description": "200g paneer or tofu, sweet potato, mixed salad"},
        ]
    },
    2: {  # Low Carb
        "meals": [
            {"time": "Breakfast (7–8 AM)",     "name": "Scrambled Eggs & Avocado", "description": "3 eggs scrambled with butter, half avocado, no bread"},
            {"time": "Mid-Morning (10–11 AM)", "name": "Cheese & Cucumber",         "description": "30g cheese cubes + cucumber sticks — keeps blood sugar stable"},
            {"time": "Lunch (1–2 PM)",         "name": "Chicken Salad",             "description": "200g chicken, leafy greens, olive oil dressing, seeds"},
            {"time": "Pre-Workout (4–5 PM)",   "name": "Boiled Eggs",               "description": "2 boiled eggs — clean protein with minimal carbs"},
            {"time": "Dinner (7–8 PM)",        "name": "Stir-Fry Vegetables",       "description": "150g chicken/paneer, zucchini, capsicum, spinach in olive oil"},
        ]
    },
    3: {  # Plant-Based
        "meals": [
            {"time": "Breakfast (7–8 AM)",     "name": "Smoothie Bowl",             "description": "Banana + berries + plant protein + chia seeds + granola"},
            {"time": "Mid-Morning (10–11 AM)", "name": "Hummus & Veggies",           "description": "3 tbsp hummus + carrot sticks + cucumber — fibre + healthy fats"},
            {"time": "Lunch (1–2 PM)",         "name": "Lentil Dal & Quinoa",        "description": "1 cup red lentils, 1 cup quinoa, roasted vegetables"},
            {"time": "Pre-Workout (4–5 PM)",   "name": "Dates & Peanut Butter",      "description": "4 dates + 1 tbsp almond butter — fast carbs + healthy fats"},
            {"time": "Dinner (7–8 PM)",        "name": "Tofu & Brown Rice",          "description": "150g tofu stir-fried in sesame oil, 1 cup brown rice, broccoli"},
        ]
    },
    4: {  # Keto
        "meals": [
            {"time": "Breakfast (7–8 AM)",     "name": "Butter Coffee & Eggs",      "description": "2 eggs, 30g butter, bulletproof coffee (butter + MCT oil)"},
            {"time": "Mid-Morning (10–11 AM)", "name": "Cheese & Olives",            "description": "40g cheese + 10 olives — pure fat and protein, zero carbs"},
            {"time": "Lunch (1–2 PM)",         "name": "Chicken Thighs & Salad",     "description": "200g chicken thighs (skin-on), full-fat dressing, leafy greens"},
            {"time": "Pre-Workout (4–5 PM)",   "name": "Almonds & Peanut Butter",    "description": "20 almonds + 1 tbsp PB — keto-friendly pre-workout energy"},
            {"time": "Dinner (7–8 PM)",        "name": "Salmon & Broccoli",          "description": "200g salmon fillet, 1 cup broccoli in butter, no grains"},
        ]
    },
}

# ── Macro ratio database ───────────────────────────────────────
MACRO_RATIOS = {
    0: {"protein": 0.30, "carbs": 0.45, "fats": 0.25},  # Balanced
    1: {"protein": 0.40, "carbs": 0.35, "fats": 0.25},  # High Protein
    2: {"protein": 0.35, "carbs": 0.20, "fats": 0.45},  # Low Carb
    3: {"protein": 0.25, "carbs": 0.55, "fats": 0.20},  # Plant-Based
    4: {"protein": 0.25, "carbs": 0.05, "fats": 0.70},  # Keto
}

# ── Weekly schedule templates ──────────────────────────────────
SCHEDULES = {
    "Cardio Focus": [
        {"day": "Mon", "focus": "Cardio 45min",   "type": "active"},
        {"day": "Tue", "focus": "Rest / Walk",    "type": "rest"},
        {"day": "Wed", "focus": "Cardio 40min",   "type": "active"},
        {"day": "Thu", "focus": "Light Yoga",     "type": "active"},
        {"day": "Fri", "focus": "Cardio 45min",   "type": "active"},
        {"day": "Sat", "focus": "Long Walk",      "type": "active"},
        {"day": "Sun", "focus": "Rest",           "type": "rest"},
    ],
    "Strength — Beginner": [
        {"day": "Mon", "focus": "Full Body A",    "type": "active"},
        {"day": "Tue", "focus": "Rest",           "type": "rest"},
        {"day": "Wed", "focus": "Full Body B",    "type": "active"},
        {"day": "Thu", "focus": "Light Cardio",   "type": "active"},
        {"day": "Fri", "focus": "Full Body A",    "type": "active"},
        {"day": "Sat", "focus": "Active Rest",    "type": "rest"},
        {"day": "Sun", "focus": "Rest",           "type": "rest"},
    ],
    "Strength — Advanced": [
        {"day": "Mon", "focus": "Push Day",       "type": "active"},
        {"day": "Tue", "focus": "Pull Day",       "type": "active"},
        {"day": "Wed", "focus": "Leg Day",        "type": "active"},
        {"day": "Thu", "focus": "Rest",           "type": "rest"},
        {"day": "Fri", "focus": "Upper Body",     "type": "active"},
        {"day": "Sat", "focus": "Lower Body",     "type": "active"},
        {"day": "Sun", "focus": "Rest",           "type": "rest"},
    ],
    "HIIT": [
        {"day": "Mon", "focus": "HIIT Circuit",   "type": "active"},
        {"day": "Tue", "focus": "Active Recovery","type": "rest"},
        {"day": "Wed", "focus": "HIIT Sprints",   "type": "active"},
        {"day": "Thu", "focus": "Strength",       "type": "active"},
        {"day": "Fri", "focus": "HIIT Circuit",   "type": "active"},
        {"day": "Sat", "focus": "Long Walk",      "type": "active"},
        {"day": "Sun", "focus": "Rest",           "type": "rest"},
    ],
    "Yoga / Mobility": [
        {"day": "Mon", "focus": "Yoga Flow",      "type": "active"},
        {"day": "Tue", "focus": "Mobility",       "type": "active"},
        {"day": "Wed", "focus": "Yoga Flow",      "type": "active"},
        {"day": "Thu", "focus": "Rest",           "type": "rest"},
        {"day": "Fri", "focus": "Yin Yoga",       "type": "active"},
        {"day": "Sat", "focus": "Hike / Walk",    "type": "active"},
        {"day": "Sun", "focus": "Rest",           "type": "rest"},
    ],
}

EXERCISE_CAT_NAMES = {
    0: "Cardio Focus",
    1: "Strength — Beginner",
    2: "Strength — Advanced",
    3: "HIIT",
    4: "Yoga / Mobility",
}

DIET_CAT_NAMES = {
    0: "Balanced",
    1: "High Protein",
    2: "Low Carb",
    3: "Plant-Based",
    4: "Keto",
}


class FitMindMLEngine:
    def __init__(self):
        self.diet_clf     = joblib.load(MODELS_DIR / "diet_classifier.pkl")
        self.exercise_clf = joblib.load(MODELS_DIR / "exercise_classifier.pkl")
        self.calorie_reg  = joblib.load(MODELS_DIR / "calorie_regressor.pkl")
        self.scaler       = joblib.load(MODELS_DIR / "scaler.pkl")

    def _encode_activity(self, activity: str) -> int:
        mapping = {
            "Sedentary": 0, "Lightly Active": 1, "Moderately Active": 2,
            "Very Active": 3, "Extremely Active": 4, "Athlete": 5,
        }
        return mapping.get(activity, 2)

    def _encode_goal(self, goal: str) -> int:
        mapping = {
            "Weight Loss": 0, "Weight Gain": 1,
            "Muscle Gain": 2, "Body Building": 3,
        }
        return mapping.get(goal, 0)

    def _encode_diet_pref(self, diets: list) -> int:
        if "High Protein" in diets: return 4
        if "Keto" in diets:         return 3
        if "Vegan" in diets:        return 2
        if "Vegetarian" in diets:   return 1
        return 0

    def _encode_gender(self, gender: str) -> int:
        return 1 if gender == "Female" else 0

    def _encode_sleep(self, sleep: str) -> float:
        mapping = {
            "Less than 5": 4.5, "5–6": 5.5, "6–7": 6.5, "7–8": 7.5, "8+": 8.5
        }
        return mapping.get(sleep, 7.0)
    
    def predict(self, user: dict) -> dict:
        import pandas as pd

        # Encode raw inputs
        age       = float(user["age"])
        height    = float(user["height"])
        weight    = float(user["weight"])
        gender    = self._encode_gender(user.get("gender", "Male"))
        bmi       = weight / (height / 100) ** 2
        activity  = self._encode_activity(user.get("activity", "Moderately Active"))
        goal_enc  = self._encode_goal(user.get("goal", "Weight Loss"))
        diet_pref = self._encode_diet_pref(user.get("diets", []))
        sleep     = self._encode_sleep(user.get("sleep", "7–8"))
        wfreq     = float(min(activity + 1, 6))

        # Derived features
        bmi_cat = 0 if bmi < 18.5 else 1 if bmi < 25 else 2 if bmi < 30 else 3
        age_grp = 0 if age < 25 else 1 if age < 35 else 2 if age < 45 else 3 if age < 60 else 4
        whr     = round(weight / height, 4)
        act_x_g = float(activity * goal_enc)
        bmi_x_g = round(bmi * goal_enc, 2)
        good_sl = 1 if sleep >= 7 else 0
        hi_bmi  = 1 if bmi > 30 else 0
        lo_bmi  = 1 if bmi < 18.5 else 0

        # Named DataFrame
        feature_names = joblib.load(MODELS_DIR / "feature_names.pkl")
        X = pd.DataFrame([[
            age, height, weight, gender, bmi,
            activity, goal_enc, diet_pref, sleep, wfreq,
            bmi_cat, age_grp, whr,
            act_x_g, bmi_x_g, good_sl, hi_bmi, lo_bmi
        ]], columns=feature_names)
        X_s = self.scaler.transform(X)

        diet_cat     = int(self.diet_clf.predict(X_s)[0])
        exercise_cat = int(self.exercise_clf.predict(X_s)[0])
        calories     = int(round(self.calorie_reg.predict(X_s)[0]))

        # Macro calculation
        ratios = MACRO_RATIOS[diet_cat]
        protein_g = round(calories * ratios["protein"] / 4)
        carbs_g   = round(calories * ratios["carbs"]   / 4)
        fats_g    = round(calories * ratios["fats"]    / 9)

        # Exercise selection — pick best 6 for the goal
        goal_str    = user.get("goal", "Weight Loss")
        ex_cat_name = EXERCISE_CAT_NAMES[exercise_cat]
        exercises_pool = (
            EXERCISE_DB.get(exercise_cat, {}).get(goal_str)
            or EXERCISE_DB.get(exercise_cat, {}).get("Weight Loss", [])
            or [{"name": "Walking", "sets": "30 min daily", "tip": "Start simple and build up"}]
        )
        exercises = exercises_pool[:6]

        # Meal plan — respect user's actual diet preferences
        diets = user.get("diets", [])
        non_veg_allowed = "Non-Vegetarian" in diets
        if not non_veg_allowed:
            # Force plant-based or balanced veg meal plan
            if "Vegan" in diets:
                meals = MEAL_DB[3]["meals"]   # Plant-Based
            elif "Keto" in diets:
                meals = MEAL_DB[4]["meals"]   # Keto (already veg-compatible)
            else:
                meals = MEAL_DB[0]["meals"]   # Balanced vegetarian
        else:
            meals = MEAL_DB[diet_cat]["meals"]

        # Weekly schedule
        schedule = SCHEDULES.get(ex_cat_name, SCHEDULES["Cardio Focus"])

        # Tips
        tips = self._build_tips(user, bmi, diet_cat, exercise_cat, calories)

        return {
            "bmi":              round(bmi, 1),
            "bmr":              self._calc_bmr(weight, height, age, gender),
            "tdee":             calories,
            "targetCalories":   calories,
            "dietCategory":     DIET_CAT_NAMES[diet_cat],
            "exerciseCategory": ex_cat_name,
            "macros": {"protein": protein_g, "carbs": carbs_g, "fats": fats_g},
            "meals":            meals,
            "exercises":        exercises,
            "weeklySchedule":   schedule,
            "tips":             tips,
            "waterTarget":      self._water_target(weight, activity),
            "sleepAdvice":      self._sleep_advice(user.get("sleep", "7–8"), goal_str),
            "greeting":         self._greeting(user.get("name", "there"), goal_str, bmi),
            "bmiInsight":       self._bmi_insight(bmi, goal_str),
        }

    def _calc_bmr(self, weight, height, age, gender):
        base = 10 * weight + 6.25 * height - 5 * age
        return int(base - 161 if gender == 1 else base + 5)

    def _water_target(self, weight, activity):
        base = weight * 0.033
        extra = activity * 0.2
        return f"{round(base + extra, 1)}L per day"

    def _sleep_advice(self, sleep, goal):
        if goal in ["Muscle Gain", "Body Building"]:
            return "Aim for 8–9 hours — growth hormone peaks during deep sleep"
        if sleep in ["Less than 5", "5–6"]:
            return "Increase to 7–8 hours — poor sleep raises cortisol and blocks fat loss"
        return "Maintain 7–8 hours — optimal for recovery and hormonal balance"

    def _greeting(self, name, goal, bmi):
        msgs = {
            "Weight Loss":   f"Hey {name}! Let's burn that fat and build a healthier you. Your plan is designed to create a sustainable calorie deficit while keeping you energized.",
            "Weight Gain":   f"Welcome {name}! Time to pack on some healthy mass. Your plan focuses on a calorie surplus with the right nutrients to fuel clean gains.",
            "Muscle Gain":   f"Let's get those gains, {name}! Your plan targets progressive overload and protein timing to maximize muscle protein synthesis.",
            "Body Building": f"Time to sculpt, {name}! Your advanced plan is built around hypertrophy principles — high volume, strategic rest, and precision nutrition.",
        }
        return msgs.get(goal, f"Welcome {name}! Here's your personalized fitness plan.")

    def _bmi_insight(self, bmi, goal):
        cat = "underweight" if bmi < 18.5 else "healthy range" if bmi < 25 else "overweight" if bmi < 30 else "obese range"
        return f"Your BMI of {round(bmi,1)} places you in the {cat}. " + {
            "Weight Loss":   "A moderate calorie deficit combined with cardio will help bring this into the healthy range.",
            "Weight Gain":   "A calorie surplus with strength training will build healthy mass and improve your BMI.",
            "Muscle Gain":   "Strength training and protein-rich diet will recompose your body — muscle replaces fat.",
            "Body Building": "Your advanced training split will optimize muscle hypertrophy and body composition.",
        }.get(goal, "Your plan is tailored to help you reach your optimal weight.")

    def _build_tips(self, user, bmi, diet_cat, exercise_cat, calories):
        tips = []
        goal = user.get("goal", "Weight Loss")
        if goal == "Weight Loss":
            tips.append("Track your meals for the first 2 weeks — awareness is the biggest driver of change")
            tips.append("Eat protein first at every meal — it reduces hunger and preserves muscle during deficit")
        elif goal in ["Muscle Gain", "Body Building"]:
            tips.append("Progressive overload is key — add 2.5kg to your lifts every 1–2 weeks")
            tips.append("Eat within 30 minutes post-workout — your muscles are most receptive then")
        elif goal == "Weight Gain":
            tips.append("Eat every 3 hours even if you're not hungry — frequency builds the calorie surplus")
        tips.append("Stay consistent — 80% adherence to a good plan beats 100% adherence to a perfect plan for 2 weeks")
        tips.append(f"Your daily calorie target is {calories} kcal — use a free app like MyFitnessPal to track")
        tips.append("Sleep is non-negotiable — more than 80% of muscle repair happens during sleep")
        return tips[:5]


# Singleton instance (loaded once on server start)
_engine = None

def get_engine() -> FitMindMLEngine:
    global _engine
    if _engine is None:
        _engine = FitMindMLEngine()
    return _engine
