# FitMind AI — Full Stack (React + Python ML)

A full-stack AI fitness app with a real **scikit-learn ML backend** and a **React + Vite** frontend.

---

## 📁 Project Structure

```
fitmind-fullstack/
├── backend/
│   ├── train_model.py      ← Generate dataset & train ML models (run once)
│   ├── ml_engine.py        ← ML inference engine + exercise/diet databases
│   ├── main.py             ← FastAPI server (REST API)
│   ├── requirements.txt    ← Python dependencies
│   └── models/             ← Auto-created after training
│       ├── diet_classifier.pkl
│       ├── exercise_classifier.pkl
│       ├── calorie_regressor.pkl
│       ├── scaler.pkl
│       └── label_maps.json
│
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx               ← Root — calls ML backend
        ├── index.css
        ├── components/
        │   ├── Navbar.jsx
        │   ├── LoadingOverlay.jsx
        │   ├── ProfileForm.jsx   ← User input (diet tiles, goals, etc.)
        │   ├── ResultsPanel.jsx  ← Plan display
        │   └── HistoryPanel.jsx
        ├── hooks/
        │   └── useHistory.js     ← localStorage history hook
        └── utils/
            ├── api.js            ← Calls http://localhost:8000
            └── calculations.js   ← BMI, BMR, TDEE
```

---

## 🤖 ML Models

| Model | Type | Predicts |
|---|---|---|
| `diet_classifier` | Random Forest Classifier | Diet category (Balanced / High Protein / Low Carb / Plant-Based / Keto) |
| `exercise_classifier` | Random Forest Classifier | Exercise type (Cardio / Strength Beginner / Strength Advanced / HIIT / Yoga) |
| `calorie_regressor` | Random Forest Regressor | Daily calorie target (kcal) |

**Input features:** age, height, weight, gender, BMI, activity level, fitness goal, diet preference, sleep hours

**Training data:** 5,000 synthetic samples generated using physics-based formulas (Mifflin-St Jeor BMR, TDEE multipliers) with realistic noise

---

## 🚀 Setup & Run

### Step 1 — Backend (Python)

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Train ML models (run ONCE — creates the models/ folder)
python train_model.py

# Start the API server
uvicorn main:app --reload --port 8000
```

API runs at: **http://localhost:8000**
Interactive docs: **http://localhost:8000/docs**

---

### Step 2 — Frontend (React)

Open a **new terminal tab** and:

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

App runs at: **http://localhost:5173**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/predict` | Get ML-powered fitness plan |

### POST /predict — Request body example:
```json
{
  "name": "Arjun Sharma",
  "age": 25,
  "gender": "Male",
  "height": 175,
  "weight": 80,
  "targetWeight": 70,
  "diets": ["High Protein"],
  "goal": "Weight Loss",
  "activity": "Moderately Active",
  "sleep": "7–8"
}
```

---

## ✨ How the ML Pipeline Works

```
User Input (React Form)
        ↓
FastAPI validates with Pydantic
        ↓
Feature encoding (gender, activity level, goal, diet pref → numeric)
        ↓
StandardScaler normalizes features
        ↓
Random Forest Classifier → diet_category (0–4)
Random Forest Classifier → exercise_category (0–4)
Random Forest Regressor  → calorie_target (kcal)
        ↓
Rule-based lookup:
  diet_category → meal plan + macro ratios
  exercise_category + goal → exercise list (6 exercises)
  exercise_category → weekly schedule
        ↓
JSON response → React renders plan
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, vanilla CSS |
| Backend | FastAPI, Uvicorn |
| ML | scikit-learn (Random Forest), NumPy, Pandas |
| Data | Synthetic dataset (5,000 samples) |
| Storage | Browser localStorage (history) |
