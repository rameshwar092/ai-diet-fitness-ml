import React from 'react'

export default function ResultsPanel({ plan, onBack, onSave }) {
  if (!plan) return (
    <div style={styles.empty}>
      <p>No plan generated yet.</p>
      <button style={styles.backBtn} onClick={onBack}>← Go to Profile</button>
    </div>
  )

  const weightDiff = plan.targetWeight
    ? (parseFloat(plan.targetWeight) - parseFloat(plan.weight)).toFixed(1)
    : null

  const p = plan.macros.protein, c = plan.macros.carbs, f = plan.macros.fats
  const cal = plan.targetCalories
  const proteinPct = Math.round((p * 4 / cal) * 100)
  const carbsPct   = Math.round((c * 4 / cal) * 100)
  const fatsPct    = Math.round((f * 9 / cal) * 100)
  const diffLabel  = weightDiff ? (weightDiff > 0 ? '+' : '') + weightDiff + 'kg' : plan.goal

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h2 style={styles.title}>Your Personalized Plan</h2>
        <p style={styles.subtitle}>{plan.name} · {plan.goal} · {plan.activity}</p>
      </div>

      {/* Greeting */}
      <div style={styles.greetingCard}>
        <p style={styles.greeting}>{plan.greeting}</p>
        <p style={styles.bmiInsight}>{plan.bmiInsight}</p>
      </div>

      {/* Stats */}
      <div style={styles.statsRow}>
        {[
          { value: plan.bmi,                    label: 'BMI' },
          { value: cal.toLocaleString(),         label: 'Daily Calories' },
          { value: plan.bmr.toLocaleString(),    label: 'BMR' },
          { value: diffLabel,                    label: weightDiff ? 'Target Change' : 'Your Goal' },
        ].map(s => (
          <div key={s.label} style={styles.statCard}>
            <div style={styles.statValue}>{s.value}</div>
            <div style={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>

      {/* Grid */}
      <div style={styles.grid}>

        {/* Meals */}
        <ResultCard title="🥗 Daily Meal Plan" iconClass="icon-green">
          {plan.meals.map((m, i) => (
            <div key={i} style={styles.mealItem}>
              <div style={styles.mealDot} />
              <div>
                <div style={styles.mealTime}>{m.time}</div>
                <div style={styles.mealName}>{m.name}</div>
                <div style={styles.mealDesc}>{m.description}</div>
              </div>
            </div>
          ))}
        </ResultCard>

        {/* Macros */}
        <ResultCard title="📊 Macros & Nutrition" iconClass="icon-blue">
          <MacroBar label="Protein"       value={p} pct={proteinPct} color="#00e5a0" />
          <MacroBar label="Carbohydrates" value={c} pct={carbsPct}   color="#0088ff" />
          <MacroBar label="Healthy Fats"  value={f} pct={fatsPct}    color="#ff6b35" />
          <div style={styles.miniCards}>
            <div style={styles.miniCard}>
              <div style={styles.miniIcon}>💧</div>
              <div style={styles.miniValue}>{plan.waterTarget}</div>
              <div style={styles.miniLabel}>Water Goal</div>
            </div>
            <div style={styles.miniCard}>
              <div style={styles.miniIcon}>😴</div>
              <div style={styles.miniValue}>{plan.sleepAdvice.split(' ').slice(0, 4).join(' ')}</div>
              <div style={styles.miniLabel}>Sleep Goal</div>
            </div>
          </div>
        </ResultCard>

        {/* Weekly Schedule */}
        <ResultCard title="📅 Weekly Training Schedule" iconClass="icon-purple" full>
          <div style={styles.weekRow}>
            {plan.weeklySchedule.map(d => (
              <div key={d.day} style={{ ...styles.weekDay, opacity: d.type === 'rest' ? 0.5 : 1 }}>
                <div style={styles.dayName}>{d.day}</div>
                <div style={{ ...styles.dayFocus, color: d.type === 'rest' ? 'var(--muted)' : 'var(--accent)' }}>{d.focus}</div>
              </div>
            ))}
          </div>
        </ResultCard>

        {/* Exercises */}
        <ResultCard title={`🏋️ Recommended Exercises for ${plan.goal}`} iconClass="icon-orange" full>
          {plan.exercises.map((e, i) => (
            <div key={i} style={styles.exerciseItem}>
              <div style={styles.exerciseNum}>{i + 1}</div>
              <div>
                <div style={styles.exerciseName}>{e.name}</div>
                <div style={styles.exerciseDetail}>{e.sets} · {e.tip}</div>
              </div>
            </div>
          ))}
        </ResultCard>

        {/* Tips */}
        <ResultCard title="💡 Personalized Tips" iconClass="icon-green" full>
          {plan.tips.map((t, i) => (
            <div key={i} style={styles.tipItem}>{t}</div>
          ))}
        </ResultCard>
      </div>

      {/* Actions */}
      <div style={styles.actions}>
        <button style={styles.backBtn}  onClick={onBack}>← Edit Profile</button>
        <button style={styles.saveBtn}  onClick={onSave}>💾 Save to History</button>
      </div>
      <div style={{ height: 40 }} />
    </div>
  )
}

// ── Sub-components ────────────────────────────────────────────
function ResultCard({ title, iconClass, children, full }) {
  return (
    <div style={{ ...styles.card, ...(full ? styles.cardFull : {}) }}>
      <h3 style={styles.cardTitle}>
        <span style={{ ...styles.iconBox, ...styles[iconClass] }} />
        {title}
      </h3>
      {children}
    </div>
  )
}

function MacroBar({ label, value, pct, color }) {
  return (
    <div style={{ marginBottom: 14 }}>
      <div style={styles.macroLabel}>
        <span style={{ fontWeight: 600 }}>{label}</span>
        <span style={{ color: 'var(--muted)' }}>{value}g · {pct}%</span>
      </div>
      <div style={styles.barTrack}>
        <div style={{ ...styles.barFill, width: `${pct}%`, background: color }} />
      </div>
    </div>
  )
}

// ── Styles ────────────────────────────────────────────────────
const styles = {
  container:   { maxWidth: 960, margin: '0 auto', padding: '0 20px', position: 'relative', zIndex: 1 },
  empty:       { textAlign: 'center', padding: 60, color: 'var(--muted)' },
  header:      { textAlign: 'center', padding: '50px 20px 30px' },
  title:       { fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '2rem' },
  subtitle:    { color: 'var(--muted)', marginTop: 8 },

  greetingCard: {
    background: 'linear-gradient(135deg,rgba(0,229,160,0.08),rgba(0,136,255,0.05))',
    border: '1px solid rgba(0,229,160,0.2)',
    borderRadius: 20, padding: 28, marginBottom: 24, animation: 'fadeUp 0.4s ease both',
  },
  greeting:   { fontSize: '1.05rem', lineHeight: 1.7 },
  bmiInsight: { color: 'var(--muted)', marginTop: 10, fontSize: '0.9rem' },

  statsRow: { display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 14, marginBottom: 24 },
  statCard: { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 16, padding: '20px 16px', textAlign: 'center' },
  statValue: { fontFamily: 'Syne, sans-serif', fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent)' },
  statLabel: { fontSize: '0.75rem', color: 'var(--muted)', marginTop: 4, fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.05em' },

  grid:     { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 24 },
  card:     { background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 20, padding: 28, boxShadow: 'var(--glow)' },
  cardFull: { gridColumn: 'span 2' },
  cardTitle: { fontFamily: 'Syne, sans-serif', fontSize: '1rem', fontWeight: 700, marginBottom: 18, display: 'flex', alignItems: 'center', gap: 10 },

  iconBox:       { width: 32, height: 32, borderRadius: 8, flexShrink: 0 },
  'icon-green':  { background: 'rgba(0,229,160,0.15)' },
  'icon-blue':   { background: 'rgba(0,136,255,0.15)' },
  'icon-orange': { background: 'rgba(255,107,53,0.15)' },
  'icon-purple': { background: 'rgba(168,85,247,0.15)' },

  mealItem: { display: 'flex', alignItems: 'flex-start', gap: 12, padding: '12px 0', borderBottom: '1px solid var(--border)' },
  mealDot:  { width: 8, height: 8, borderRadius: '50%', background: 'var(--accent)', marginTop: 6, flexShrink: 0 },
  mealTime: { fontSize: '0.7rem', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 2 },
  mealName: { fontWeight: 600, fontSize: '0.9rem' },
  mealDesc: { color: 'var(--muted)', fontSize: '0.8rem', marginTop: 2 },

  macroLabel: { display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: 6 },
  barTrack:   { background: 'var(--surface2)', borderRadius: 50, height: 8, overflow: 'hidden' },
  barFill:    { height: '100%', borderRadius: 50, transition: 'width 1s ease' },

  miniCards:  { display: 'flex', gap: 12, flexWrap: 'wrap', marginTop: 20, paddingTop: 16, borderTop: '1px solid var(--border)' },
  miniCard:   { background: 'var(--surface2)', borderRadius: 10, padding: '12px 16px', flex: 1, textAlign: 'center' },
  miniIcon:   { fontSize: '1.2rem' },
  miniValue:  { fontWeight: 700, fontSize: '0.9rem', marginTop: 4 },
  miniLabel:  { color: 'var(--muted)', fontSize: '0.72rem' },

  weekRow:   { display: 'flex', gap: 8, flexWrap: 'wrap' },
  weekDay:   { flex: 1, minWidth: 80, background: 'var(--surface2)', borderRadius: 10, padding: '12px 8px', textAlign: 'center' },
  dayName:   { color: 'var(--muted)', fontWeight: 600, fontSize: '0.7rem', textTransform: 'uppercase', marginBottom: 6 },
  dayFocus:  { fontWeight: 700, fontSize: '0.8rem' },

  exerciseItem:   { background: 'var(--surface2)', borderRadius: 12, padding: 14, marginBottom: 10, display: 'flex', alignItems: 'center', gap: 14 },
  exerciseNum:    { width: 28, height: 28, borderRadius: 8, background: 'rgba(0,136,255,0.15)', color: 'var(--accent2)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: 800, flexShrink: 0 },
  exerciseName:   { fontWeight: 600, fontSize: '0.88rem' },
  exerciseDetail: { color: 'var(--muted)', fontSize: '0.78rem', marginTop: 2 },

  tipItem: { display: 'flex', alignItems: 'flex-start', gap: 10, padding: '10px 0', borderBottom: '1px solid var(--border)', fontSize: '0.85rem', color: 'var(--muted)', lineHeight: 1.5 },

  actions: { display: 'flex', gap: 12, marginTop: 8 },
  backBtn: { flex: 1, background: 'var(--surface2)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 12, padding: '12px 24px', fontSize: '0.9rem', fontWeight: 500, transition: 'all 0.2s' },
  saveBtn: { flex: 1, background: 'var(--accent)', color: '#000', border: 'none', borderRadius: 12, padding: '12px 24px', fontFamily: 'Syne, sans-serif', fontSize: '0.95rem', fontWeight: 700, transition: 'all 0.2s' },
}
