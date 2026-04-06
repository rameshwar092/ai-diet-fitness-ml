import React, { useEffect, useState } from 'react'

const MESSAGES = [
  'Analyzing your profile...',
  'Calculating your metabolic rate...',
  'Building your workout plan...',
  'Crafting your meal recommendations...',
  'Optimizing for your goals...',
]

export default function LoadingOverlay({ show }) {
  const [msgIdx, setMsgIdx] = useState(0)

  useEffect(() => {
    if (!show) return
    setMsgIdx(0)
    const id = setInterval(() => setMsgIdx(i => (i + 1) % MESSAGES.length), 1200)
    return () => clearInterval(id)
  }, [show])

  if (!show) return null

  return (
    <div style={styles.overlay}>
      <div style={styles.spinner} />
      <p style={styles.text}>{MESSAGES[msgIdx]}</p>
    </div>
  )
}

const styles = {
  overlay: {
    position: 'fixed',
    inset: 0,
    background: 'rgba(11,15,26,0.92)',
    backdropFilter: 'blur(10px)',
    zIndex: 200,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 20,
  },
  spinner: {
    width: 56,
    height: 56,
    borderRadius: '50%',
    border: '3px solid var(--border)',
    borderTopColor: 'var(--accent)',
    animation: 'spin 0.9s linear infinite',
  },
  text: {
    color: 'var(--muted)',
    fontSize: '0.95rem',
    animation: 'pulse 1.8s ease-in-out infinite',
  },
}
