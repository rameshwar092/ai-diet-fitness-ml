import React, { useState } from 'react'

// ── Tile data ────────────────────────────────────────────────
const DIET_OPTIONS = [
  { id: 'Vegetarian',     label: '🥦 Vegetarian' },
  { id: 'Vegan',          label: '🌱 Vegan' },
  { id: 'Non-Vegetarian', label: '🍗 Non-Vegetarian' },
  { id: 'Gluten-Free',    label: '🌾 Gluten-Free' },
  { id: 'Dairy-Free',     label: '🥛 Dairy-Free' },
  { id: 'High Protein',   label: '💪 High Protein' },
]

const GOAL_OPTIONS = [
  { id: 'Weight Loss',   icon: '🔥', label: 'Weight Loss' },
  { id: 'Weight Gain',   icon: '📈', label: 'Weight Gain' },
  { id: 'Muscle Gain',   icon: '💪', label: 'Muscle Gain' },
  { id: 'Body Building', icon: '🏋️', label: 'Body Building' },
]

const ACTIVITY_OPTIONS = [
  { id: 'Sedentary',         label: '😴 Sedentary',         sub: 'Desk job, little movement' },
  { id: 'Lightly Active',    label: '🚶 Lightly Active',    sub: '1–2 days/week' },
  { id: 'Moderately Active', label: '🏃 Moderately Active', sub: '3–4 days/week' },
  { id: 'Very Active',       label: '⚡ Very Active',        sub: '5–6 days/week' },
  { id: 'Extremely Active',  label: '🔥 Extremely Active',  sub: 'Daily intense training' },
  { id: 'Athlete',           label: '🏅 Athlete',            sub: 'Professional training' },
]

// ── Reusable sub-components ──────────────────────────────────
function FormCard({ children, title, delay = 0 }) {
  return (
    <div style={{ ...styles.card, animationDelay: `${delay}s` }}>
      {title && <h2 style={styles.cardTitle}>{title}</h2>}
      {children}
    </div>
  )
}

function Field({ label, hint, children, full }) {
  return (
    <div style={{ ...styles.field, ...(full ? styles.fieldFull : {}) }}>
      <label style={styles.label}>
        {label}
        {hint && <span style={styles.labelHint}> {hint}</span>}
      </label>
      {children}
    </div>
  )
}

function Input({ ...props }) {
  const [focused, setFocused] = useState(false)
  return (
    <input
      style={{ ...styles.input, ...(focused ? styles.inputFocus : {}) }}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      {...props}
    />
  )
}

function Select({ children, ...props }) {
  const [focused, setFocused] = useState(false)
  return (
    <select
      style={{ ...styles.input, ...(focused ? styles.inputFocus : {}) }}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      {...props}
    >
      {children}
    </select>
  )
}

// ── Main component ───────────────────────────────────────────
export default function ProfileForm({ onSubmit, loading }) {
  const [form, setForm] = useState({
    name: '', age: '', gender: '', height: '', weight: '',
    targetWeight: '', allergies: '', medical: '', sleep: '', water: '', workoutDuration: '',
  })
  const [selectedDiets,    setSelectedDiets]    = useState([])
  const [selectedGoal,     setSelectedGoal]     = useState('')
  const [selectedActivity, setSelectedActivity] = useState('')

  const set = (key, val) => setForm(f => ({ ...f, [key]: val }))

  const toggleDiet = (id) =>
    setSelectedDiets(d => d.includes(id) ? d.filter(x => x !== id) : [...d, id])

  const handleSubmit = () => {
    if (!form.name || !form.age || !form.gender || !form.height || !form.weight || !selectedGoal || !selectedActivity) {
      alert('Please fill in all required fields and select your goal & activity level.')
      return
    }
    onSubmit({ ...form, diets: selectedDiets, goal: selectedGoal, activity: selectedActivity })
  }

  return (
    <div style={styles.container}>

      {/* HERO */}
      <div style={styles.hero}>
        <div style={styles.badge}>⚡ AI-Powered Fitness</div>
        <h1 style={styles.heroTitle}>
          Your Personal <em style={{ color: 'var(--accent)', fontStyle: 'normal' }}>AI Coach</em>
          <br />Starts Here
        </h1>
        <p style={styles.heroSub}>Tell us about yourself and your goals. Our AI builds a plan just for you.</p>
      </div>

      {/* PERSONAL INFO */}
      <FormCard title="👤 Personal Information" delay={0}>
        <div style={styles.grid}>
          <Field label="Full Name"><Input id="name" placeholder="e.g. Rameshwar" value={form.name} onChange={e => set('name', e.target.value)} /></Field>
          <Field label="Age"><Input id="age" type="number" placeholder="25" min="10" max="100" value={form.age} onChange={e => set('age', e.target.value)} /></Field>
          <Field label="Gender">
            <Select value={form.gender} onChange={e => set('gender', e.target.value)}>
              <option value="">Select gender</option>
              <option>Male</option><option>Female</option><option>Other</option>
            </Select>
          </Field>
          <Field label="Height (cm)"><Input type="number" placeholder="170" min="100" max="250" value={form.height} onChange={e => set('height', e.target.value)} /></Field>
          <Field label="Weight (kg)"><Input type="number" placeholder="70" min="30" max="250" value={form.weight} onChange={e => set('weight', e.target.value)} /></Field>
          <Field label="Target Weight (kg)"><Input type="number" placeholder="65" min="30" max="250" value={form.targetWeight} onChange={e => set('targetWeight', e.target.value)} /></Field>

          {/* Diet multi-select */}
          <Field label="Diet Type" hint="(select all that apply)" full>
            <div style={styles.dietGrid}>
              {DIET_OPTIONS.map(d => (
                <button
                  key={d.id}
                  style={{ ...styles.dietTile, ...(selectedDiets.includes(d.id) ? styles.dietTileSelected : {}) }}
                  onClick={() => toggleDiet(d.id)}
                >
                  {d.label}
                </button>
              ))}
            </div>
            {/* Display box */}
            <div style={{ ...styles.dietDisplay, ...(selectedDiets.length ? styles.dietDisplayActive : {}) }}>
              {selectedDiets.length === 0
                ? <span style={styles.dietPlaceholder}> Selected diet ...</span>
                : selectedDiets.map(d => (
                    <span key={d} style={styles.dietTag}>
                      {d}
                      <button style={styles.dietTagRemove} onClick={() => toggleDiet(d)}>✕</button>
                    </span>
                  ))
              }
            </div>
          </Field>

          <Field label="Allergies / Restrictions">
            <Input placeholder="e.g. dairy, nuts (optional)" value={form.allergies} onChange={e => set('allergies', e.target.value)} />
          </Field>
        </div>
      </FormCard>

      {/* FITNESS GOAL */}
      <FormCard title="🎯 Fitness Goal" delay={0.08}>
        <div style={styles.goalGrid}>
          {GOAL_OPTIONS.map(g => (
            <button
              key={g.id}
              style={{ ...styles.goalTile, ...(selectedGoal === g.id ? styles.goalTileSelected : {}) }}
              onClick={() => setSelectedGoal(g.id)}
            >
              <div style={styles.goalIcon}>{g.icon}</div>
              <div style={{ ...styles.goalLabel, ...(selectedGoal === g.id ? { color: 'var(--accent)' } : {}) }}>{g.label}</div>
            </button>
          ))}
        </div>
      </FormCard>

      {/* ACTIVITY LEVEL */}
      <FormCard title="🏃 Activity Level" delay={0.16}>
        <div style={styles.activityGrid}>
          {ACTIVITY_OPTIONS.map(a => (
            <button
              key={a.id}
              style={{ ...styles.activityTile, ...(selectedActivity === a.id ? styles.activityTileSelected : {}) }}
              onClick={() => setSelectedActivity(a.id)}
            >
              {a.label}
              <small style={styles.activitySub}>{a.sub}</small>
            </button>
          ))}
        </div>
      </FormCard>

      {/* ADDITIONAL INFO */}
      <FormCard title="ℹ️ Additional Health Info" delay={0.24}>
        <div style={styles.grid}>
          <Field label="Medical Conditions"><Input placeholder="e.g. diabetes (optional)" value={form.medical} onChange={e => set('medical', e.target.value)} /></Field>
          <Field label="Sleep (hours/night)">
            <Select value={form.sleep} onChange={e => set('sleep', e.target.value)}>
              <option value="">Select</option>
              <option>Less than 5</option><option>5–6</option><option>6–7</option><option>7–8</option><option>8+</option>
            </Select>
          </Field>
          <Field label="Water Intake (liters/day)">
            <Select value={form.water} onChange={e => set('water', e.target.value)}>
              <option value="">Select</option>
              <option>Less than 1L</option><option>1–2L</option><option>2–3L</option><option>3L+</option>
            </Select>
          </Field>
          <Field label="Workout Duration">
            <Select value={form.workoutDuration} onChange={e => set('workoutDuration', e.target.value)}>
              <option value="">Select</option>
              <option>20–30 mins</option><option>30–45 mins</option><option>45–60 mins</option><option>60–90 mins</option><option>90+ mins</option>
            </Select>
          </Field>
        </div>
      </FormCard>

      <button style={styles.submitBtn} onClick={handleSubmit} disabled={loading}>
        ⚡ Generate My AI Plan
      </button>
      <div style={{ height: 40 }} />
    </div>
  )
}

// ── Styles ────────────────────────────────────────────────────
const styles = {
  container: { maxWidth: 960, margin: '0 auto', padding: '0 20px', position: 'relative', zIndex: 1 },
  hero: { textAlign: 'center', padding: '70px 20px 50px' },
  badge: {
    display: 'inline-flex', alignItems: 'center', gap: 8,
    background: 'rgba(0,229,160,0.1)', border: '1px solid rgba(0,229,160,0.25)',
    color: 'var(--accent)', borderRadius: 50, padding: '6px 16px',
    fontSize: '0.78rem', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase',
    marginBottom: 24,
  },
  heroTitle: { fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: 'clamp(2.2rem,6vw,3.6rem)', lineHeight: 1.1, marginBottom: 16 },
  heroSub: { color: 'var(--muted)', fontSize: '1.05rem', maxWidth: 500, margin: '0 auto' },

  card: {
    background: 'var(--surface)', border: '1px solid var(--border)',
    borderRadius: 20, padding: 36, marginBottom: 24,
    boxShadow: 'var(--glow)', animation: 'fadeUp 0.5s ease both',
  },
  cardTitle: { fontFamily: 'Syne, sans-serif', fontSize: '1.2rem', fontWeight: 700, marginBottom: 24 },

  grid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 18 },
  field: { display: 'flex', flexDirection: 'column', gap: 8 },
  fieldFull: { gridColumn: 'span 2' },
  label: { fontSize: '0.8rem', fontWeight: 600, color: 'var(--muted)', letterSpacing: '0.06em', textTransform: 'uppercase' },
  labelHint: { color: 'var(--accent)', fontSize: '0.7rem', textTransform: 'none', letterSpacing: 0 },
  input: {
    background: 'var(--surface2)', border: '1px solid var(--border)',
    color: 'var(--text)', borderRadius: 10, padding: '12px 14px',
    fontSize: '0.95rem', outline: 'none', transition: 'border-color 0.2s', width: '100%',
  },
  inputFocus: { borderColor: 'var(--accent)' },

  dietGrid: { display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 10, marginBottom: 0 },
  dietTile: {
    background: 'var(--surface2)', border: '2px solid var(--border)',
    borderRadius: 12, padding: '12px 10px', textAlign: 'center',
    fontSize: '0.83rem', fontWeight: 500, color: 'var(--text)',
    transition: 'all 0.2s',
  },
  dietTileSelected: { borderColor: 'var(--accent)', background: 'rgba(0,229,160,0.1)', color: 'var(--accent)', fontWeight: 700 },
  dietDisplay: {
    minHeight: 44, marginTop: 10,
    background: 'var(--surface2)', border: '1px solid var(--border)',
    borderRadius: 10, padding: '10px 14px',
    display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 8,
    transition: 'border-color 0.2s',
  },
  dietDisplayActive: { borderColor: 'var(--accent)' },
  dietPlaceholder: { color: 'var(--muted)', fontSize: '0.85rem', fontStyle: 'italic' },
  dietTag: {
    display: 'inline-flex', alignItems: 'center', gap: 5,
    background: 'rgba(0,229,160,0.12)', color: 'var(--accent)',
    border: '1px solid rgba(0,229,160,0.3)', borderRadius: 50,
    padding: '4px 12px', fontSize: '0.78rem', fontWeight: 600,
  },
  dietTagRemove: { background: 'none', border: 'none', color: 'inherit', cursor: 'pointer', opacity: 0.7, fontSize: '0.9rem', marginLeft: 2 },

  goalGrid: { display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 12 },
  goalTile: {
    background: 'var(--surface2)', border: '2px solid var(--border)',
    borderRadius: 14, padding: '18px 12px', textAlign: 'center',
    transition: 'all 0.2s', color: 'var(--text)',
  },
  goalTileSelected: { borderColor: 'var(--accent)', background: 'rgba(0,229,160,0.08)' },
  goalIcon: { fontSize: '1.8rem', marginBottom: 8 },
  goalLabel: { fontSize: '0.78rem', fontWeight: 600, color: 'var(--muted)' },

  activityGrid: { display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10 },
  activityTile: {
    background: 'var(--surface2)', border: '2px solid var(--border)',
    borderRadius: 12, padding: '14px 10px', textAlign: 'center',
    fontSize: '0.82rem', fontWeight: 500, color: 'var(--text)',
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4,
    transition: 'all 0.2s',
  },
  activityTileSelected: { borderColor: 'var(--accent2)', background: 'rgba(0,136,255,0.08)', color: 'var(--accent2)' },
  activitySub: { color: 'var(--muted)', fontSize: '0.75rem' },

  submitBtn: {
    background: 'var(--accent)', color: '#000',
    border: 'none', borderRadius: 12, padding: '15px 32px',
    fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '1rem',
    width: '100%', marginTop: 8, transition: 'all 0.2s',
  },
}
