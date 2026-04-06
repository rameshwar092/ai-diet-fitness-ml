"""
train_model.py — FitMind AI
============================
Algorithms:
  - Diet Classifier     → MLP Neural Network (MLPClassifier)
  - Exercise Classifier → MLP Neural Network (MLPClassifier)
  - Calorie Regressor   → HistGradientBoostingRegressor

Run:
    python train_model.py
"""

import json
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score, classification_report

np.random.seed(42)

DATA_DIR  = Path("data")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# ═══════════════════════════════════════════════════════════════
#  DETERMINISTIC LABEL FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def deterministic_diet_label(bmi, goal, diet_pref, gender, age):
    """
    Returns: 0=Balanced  1=HighProtein  2=LowCarb  3=PlantBased  4=Keto
    """
    if diet_pref in [2, 3]:        return 3   # Vegan/Vegetarian → Plant-Based
    if diet_pref == 4:             return 4   # Keto preference  → Keto
    if goal in [2, 3]:             return 1   # Muscle/BodyBuild → High Protein
    if goal == 0 and bmi >= 33:    return 4   # Obese + Loss     → Keto
    if goal == 0 and bmi >= 28:    return 2   # Overweight + Loss → Low Carb
    if goal == 1:                  return 0   # Weight Gain      → Balanced
    return 0                                  # Default          → Balanced


def deterministic_exercise_label(goal, activity, bmi, age):
    """
    Returns: 0=Cardio  1=StrBeginner  2=StrAdvanced  3=HIIT  4=Yoga
    """
    if activity == 0 and bmi > 32: return 4   # Very sedentary + obese → Yoga
    if age > 55 and activity <= 1: return 4   # Older + low activity   → Yoga
    if goal == 0:
        return 0 if activity <= 1 else 3      # Weight Loss: Cardio or HIIT
    if goal == 1:
        return 1 if activity <= 2 else 2      # Weight Gain: Strength
    if goal == 2:
        return 1 if activity <= 1 else 2      # Muscle Gain: Strength
    if goal == 3:
        return 2                              # Body Building: Strength Advanced
    return 0


def calc_bmr(weight, height_cm, age, gender):
    """Mifflin-St Jeor Equation"""
    base = 10 * weight + 6.25 * height_cm - 5 * age
    return base + 5 if gender == 0 else base - 161


def calc_calorie_target(bmr, activity, goal):
    """TDEE + goal-based adjustment"""
    multipliers = [1.2, 1.375, 1.55, 1.725, 1.9, 2.0]
    tdee = bmr * multipliers[int(activity)]
    adjustments = {0: -450, 1: 450, 2: 300, 3: 600}
    return np.clip(tdee + adjustments[int(goal)], 1200, 5500)


# ═══════════════════════════════════════════════════════════════
#  FEATURE NAMES
# ═══════════════════════════════════════════════════════════════

FEATURE_NAMES = [
    "age", "height_cm", "weight_kg", "gender_enc", "bmi",
    "activity_level", "goal", "diet_pref", "sleep_hours", "workout_freq",
    "bmi_category", "age_group", "whr",
    "activity_x_goal", "bmi_x_goal",
    "good_sleep", "high_bmi_flag", "low_bmi_flag",
]


# ═══════════════════════════════════════════════════════════════
#  DATASET GENERATION
# ═══════════════════════════════════════════════════════════════

def generate_dataset(n=15000):
    print(f"  Generating {n} samples with deterministic labels...")

    ages       = np.random.randint(16, 65, n)
    heights    = np.random.normal(170, 12, n).clip(150, 200)
    weights    = np.random.normal(72, 18, n).clip(40, 130)
    genders    = np.random.randint(0, 2, n)
    bmi        = weights / (heights / 100) ** 2
    activities = np.random.randint(0, 6, n)
    goals      = np.random.randint(0, 4, n)
    diet_pref  = np.random.randint(0, 5, n)
    sleep_hrs  = np.random.normal(7.0, 0.9, n).clip(4, 9)
    wfreq      = np.clip(activities + np.random.randint(-1, 2, n), 0, 6).astype(float)

    bmr_vals = np.array([
        calc_bmr(weights[i], heights[i], ages[i], genders[i]) for i in range(n)
    ])
    calorie_targets = np.array([
        calc_calorie_target(bmr_vals[i], activities[i], goals[i]) for i in range(n)
    ])
    diet_labels = np.array([
        deterministic_diet_label(bmi[i], goals[i], diet_pref[i], genders[i], ages[i])
        for i in range(n)
    ])
    exercise_labels = np.array([
        deterministic_exercise_label(goals[i], activities[i], bmi[i], ages[i])
        for i in range(n)
    ])

    df = pd.DataFrame({
        "age":               ages,
        "height_cm":         heights.round(1),
        "weight_kg":         weights.round(1),
        "gender_enc":        genders,
        "bmi":               bmi.round(2),
        "activity_level":    activities,
        "goal":              goals,
        "diet_pref":         diet_pref,
        "sleep_hours":       sleep_hrs.round(1),
        "workout_freq":      wfreq,
        "calorie_target":    calorie_targets.round(0),
        "diet_category":     diet_labels,
        "exercise_category": exercise_labels,
    })

    # ── Save dataset to CSV ────────────────────────────────────
    df.to_csv("data/training_dataset.csv", index=False)
    print(f"  ✅ Dataset saved to data/training_dataset.csv")

    return df


# ═══════════════════════════════════════════════════════════════
#  FEATURE ENGINEERING
# ═══════════════════════════════════════════════════════════════

def engineer_features(df):
    X = pd.DataFrame()
    X["age"]             = df["age"]
    X["height_cm"]       = df["height_cm"]
    X["weight_kg"]       = df["weight_kg"]
    X["gender_enc"]      = df["gender_enc"]
    X["bmi"]             = df["bmi"]
    X["activity_level"]  = df["activity_level"]
    X["goal"]            = df["goal"]
    X["diet_pref"]       = df["diet_pref"]
    X["sleep_hours"]     = df["sleep_hours"]
    X["workout_freq"]    = df["workout_freq"]
    X["bmi_category"]    = pd.cut(df["bmi"], bins=[0, 18.5, 25, 30, 100],
                                   labels=[0, 1, 2, 3]).astype(int)
    X["age_group"]       = pd.cut(df["age"], bins=[0, 25, 35, 45, 60, 100],
                                   labels=[0, 1, 2, 3, 4]).astype(int)
    X["whr"]             = (df["weight_kg"] / df["height_cm"]).round(4)
    X["activity_x_goal"] = (df["activity_level"] * df["goal"]).astype(float)
    X["bmi_x_goal"]      = (df["bmi"] * df["goal"]).round(2)
    X["good_sleep"]      = (df["sleep_hours"] >= 7).astype(int)
    X["high_bmi_flag"]   = (df["bmi"] > 30).astype(int)
    X["low_bmi_flag"]    = (df["bmi"] < 18.5).astype(int)
    return X[FEATURE_NAMES]


# ═══════════════════════════════════════════════════════════════
#  MAIN TRAINING PIPELINE
# ═══════════════════════════════════════════════════════════════

def train_and_save():
    print("\n" + "="*55)
    print("  FitMind AI — ML Training Pipeline")
    print("="*55)

    # ── Step 1: Load data ──────────────────────────────────────
    print("\n[1/4] Preparing dataset...")
    df = generate_dataset(n=15000)
    df = df.dropna().reset_index(drop=True)
    print(f"  Total rows: {len(df)}")
    print(f"  Diet labels:     {dict(df['diet_category'].value_counts().sort_index())}")
    print(f"  Exercise labels: {dict(df['exercise_category'].value_counts().sort_index())}")

    # ── Step 2: Feature engineering ───────────────────────────
    print("\n[2/4] Engineering features...")
    X          = engineer_features(df)
    y_diet     = df["diet_category"].astype(int)
    y_exercise = df["exercise_category"].astype(int)
    y_calories = df["calorie_target"].astype(float)

    # ── Train/test split ───────────────────────────────────────
    (X_tr, X_te,
     yd_tr, yd_te,
     ye_tr, ye_te,
     yc_tr, yc_te) = train_test_split(
        X, y_diet, y_exercise, y_calories,
        test_size=0.15, random_state=42, stratify=y_diet
    )

    scaler  = StandardScaler()
    X_tr_s  = scaler.fit_transform(X_tr)
    X_te_s  = scaler.transform(X_te)
    cv      = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # ── Step 3: Train models ───────────────────────────────────
    print("\n[3/4] Training models...")

    # Diet Classifier — MLP Neural Network
    print("\n  Diet Classifier — MLPClassifier (Neural Network)")
    diet_clf = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation="relu",
        solver="adam",
        alpha=0.001,
        batch_size=128,
        learning_rate="adaptive",
        learning_rate_init=0.001,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=20,
        random_state=42,
        verbose=False,
    )
    diet_clf.fit(X_tr_s, yd_tr)
    diet_pred = diet_clf.predict(X_te_s)
    diet_acc  = accuracy_score(yd_te, diet_pred)
    diet_cv   = cross_val_score(diet_clf, scaler.transform(X), y_diet,
                                 cv=cv, scoring="accuracy", n_jobs=-1).mean()
    print(f"  Test accuracy  : {diet_acc*100:.2f}%")
    print(f"  CV accuracy    : {diet_cv*100:.2f}%")
    print(classification_report(yd_te, diet_pred,
          target_names=["Balanced", "HighProtein", "LowCarb", "PlantBased", "Keto"],
          zero_division=0))

    # Exercise Classifier — MLP Neural Network
    print("  Exercise Classifier — MLPClassifier (Neural Network)")
    ex_clf = MLPClassifier(
        hidden_layer_sizes=(256, 128, 64),
        activation="relu",
        solver="adam",
        alpha=0.001,
        batch_size=128,
        learning_rate="adaptive",
        learning_rate_init=0.001,
        max_iter=500,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=20,
        random_state=42,
        verbose=False,
    )
    ex_clf.fit(X_tr_s, ye_tr)
    ex_pred = ex_clf.predict(X_te_s)
    ex_acc  = accuracy_score(ye_te, ex_pred)
    ex_cv   = cross_val_score(ex_clf, scaler.transform(X), y_exercise,
                               cv=cv, scoring="accuracy", n_jobs=-1).mean()
    print(f"  Test accuracy  : {ex_acc*100:.2f}%")
    print(f"  CV accuracy    : {ex_cv*100:.2f}%")
    print(classification_report(ye_te, ex_pred,
          target_names=["Cardio", "StrBeginner", "StrAdvanced", "HIIT", "Yoga"],
          zero_division=0))

    # Calorie Regressor — HistGradientBoosting
    print("  Calorie Regressor — HistGradientBoostingRegressor")
    cal_reg = HistGradientBoostingRegressor(
        max_iter=500,
        learning_rate=0.05,
        max_depth=8,
        min_samples_leaf=10,
        l2_regularization=0.1,
        max_bins=255,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=20,
    )
    cal_reg.fit(X_tr_s, yc_tr)
    cal_pred = cal_reg.predict(X_te_s)
    cal_mae  = mean_absolute_error(yc_te, cal_pred)
    cal_r2   = r2_score(yc_te, cal_pred)
    print(f"  MAE            : {cal_mae:.1f} kcal")
    print(f"  R²             : {cal_r2:.4f}")

    # ── Step 4: Save models ────────────────────────────────────
    print("\n[4/4] Saving models...")
    joblib.dump(diet_clf,      MODEL_DIR / "diet_classifier.pkl")
    joblib.dump(ex_clf,        MODEL_DIR / "exercise_classifier.pkl")
    joblib.dump(cal_reg,       MODEL_DIR / "calorie_regressor.pkl")
    joblib.dump(scaler,        MODEL_DIR / "scaler.pkl")
    joblib.dump(FEATURE_NAMES, MODEL_DIR / "feature_names.pkl")

    label_maps = {
        "diet_categories": {
            "0": "Balanced",
            "1": "High Protein",
            "2": "Low Carb",
            "3": "Plant-Based",
            "4": "Keto",
        },
        "exercise_categories": {
            "0": "Cardio Focus",
            "1": "Strength — Beginner",
            "2": "Strength — Advanced",
            "3": "HIIT",
            "4": "Yoga / Mobility",
        },
        "goals": {
            "0": "Weight Loss",
            "1": "Weight Gain",
            "2": "Muscle Gain",
            "3": "Body Building",
        },
        "activity_levels": {
            "0": "Sedentary",
            "1": "Lightly Active",
            "2": "Moderately Active",
            "3": "Very Active",
            "4": "Extremely Active",
            "5": "Athlete",
        },
    }

    meta = {
        "algorithm":              "MLP Neural Network (Diet & Exercise) + HistGradientBoosting (Calories)",
        "feature_names":          FEATURE_NAMES,
        "n_features":             len(FEATURE_NAMES),
        "training_samples":       len(df),
        "diet_test_accuracy":     round(float(diet_acc), 4),
        "diet_cv_accuracy":       round(float(diet_cv),  4),
        "exercise_test_accuracy": round(float(ex_acc),   4),
        "exercise_cv_accuracy":   round(float(ex_cv),    4),
        "calorie_mae":            round(float(cal_mae),  2),
        "calorie_r2":             round(float(cal_r2),   4),
        "label_maps":             label_maps,
    }

    with open(MODEL_DIR / "model_meta.json", "w") as f:
        json.dump(meta, f, indent=2)
    with open(MODEL_DIR / "label_maps.json", "w") as f:
        json.dump(label_maps, f, indent=2)

    print("\n" + "="*55)
    print("  Done!")
    print(f"  Algorithm      : MLP Neural Network (Diet & Exercise) + HistGradientBoosting (Calories)")
    print(f"  Diet           : {diet_acc*100:.1f}%  (CV {diet_cv*100:.1f}%)")
    print(f"  Exercise       : {ex_acc*100:.1f}%  (CV {ex_cv*100:.1f}%)")
    print(f"  Calories       : {cal_mae:.0f} kcal MAE  (R² {cal_r2:.4f})")
    print(f"  Dataset CSV    : data/training_dataset.csv")
    print("="*55 + "\n")


if __name__ == "__main__":
    train_and_save()