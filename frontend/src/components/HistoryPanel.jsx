import React from 'react'
import { formatDate } from '../utils/calculations'

export default function HistoryPanel({ history, onLoad, onClear }) {
  if (history.length === 0) {
    return (
      <div style={styles.container}>
        <Header history={history} onClear={onClear} />
        <div style={styles.empty}>
          <div style={styles.emptyIcon}>📋</div>
          <p style={{ marginBottom: 8 }}>No saved plans yet.</p>
          <p style={{ fontSize: '0.85rem' }}>Generate a plan and save it to track your progress.</p>
        </div>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <Header history={history} onClear={onClear} />
      {history.map((h, i) => {
        const cals = h.targetCalories ? h.targetCalories.toLocaleString() : '—'
        const tw   = h.targetWeight || '?'
        return (
          <div key={i} style={styles.card} onClick={() => onLoad(h)}>
            <div style={styles.cardHeader}>
              <div>
                <div style={styles.name}>{h.name}</div>
                <div style={styles.date}>{formatDate(h.savedAt)}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={styles.cals}>{cals} kcal</div>
                <div style={styles.calsLabel}>Daily Target</div>
              </div>
            </div>
            <div style={styles.tags}>
              <Tag>🎯 {h.goal}</Tag>
              <Tag color="blue">⚡ {h.activity}</Tag>
              <Tag color="orange">📏 BMI {h.bmi}</Tag>
              <Tag>{h.weight}kg → {tw}kg</Tag>
            </div>
          </div>
        )
      })}
      <div style={{ height: 40 }} />
    </div>
  )
}

function Header({ history, onClear }) {
  return (
    <div style={styles.header}>
      <div>
        <h2 style={styles.title}>History</h2>
        <p style={styles.sub}>Your previous plans and progress</p>
      </div>
      {history.length > 0 && (
        <button style={styles.clearBtn} onClick={onClear}>Clear All</button>
      )}
    </div>
  )
}

function Tag({ children, color }) {
  const colorMap = {
    blue:   { background: 'rgba(0,136,255,0.1)',  color: 'var(--accent2)', border: 'rgba(0,136,255,0.2)' },
    orange: { background: 'rgba(255,107,53,0.1)', color: 'var(--warn)',    border: 'rgba(255,107,53,0.2)' },
    default:{ background: 'rgba(0,229,160,0.1)',  color: 'var(--accent)',  border: 'rgba(0,229,160,0.2)' },
  }
  const c = colorMap[color] || colorMap.default
  return (
    <span style={{ ...styles.tag, background: c.background, color: c.color, borderColor: c.border }}>
      {children}
    </span>
  )
}

const styles = {
  container: { maxWidth: 960, margin: '0 auto', padding: '40px 20px 0', position: 'relative', zIndex: 1 },
  header:    { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 28 },
  title:     { fontFamily: 'Syne, sans-serif', fontWeight: 800, fontSize: '1.6rem' },
  sub:       { color: 'var(--muted)', fontSize: '0.9rem', marginTop: 4 },
  clearBtn:  { background: 'var(--surface2)', color: 'var(--text)', border: '1px solid var(--border)', borderRadius: 12, padding: '10px 20px', fontSize: '0.85rem', fontWeight: 500 },

  empty:     { textAlign: 'center', padding: '60px 20px', color: 'var(--muted)' },
  emptyIcon: { fontSize: '3rem', marginBottom: 16 },

  card: {
    background: 'var(--surface)', border: '1px solid var(--border)',
    borderRadius: 16, padding: 24, marginBottom: 16,
    cursor: 'pointer', transition: 'border-color 0.2s',
    animation: 'fadeUp 0.4s ease both',
  },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 14 },
  name:       { fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '1.1rem' },
  date:       { fontSize: '0.78rem', color: 'var(--muted)', marginTop: 2 },
  cals:       { fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent)' },
  calsLabel:  { fontSize: '0.75rem', color: 'var(--muted)' },

  tags: { display: 'flex', gap: 8, flexWrap: 'wrap' },
  tag:  { display: 'inline-flex', alignItems: 'center', gap: 5, borderRadius: 50, border: '1px solid', padding: '4px 12px', fontSize: '0.72rem', fontWeight: 600 },
}
