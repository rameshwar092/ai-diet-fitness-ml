import React from 'react'

const TABS = ['Profile', 'Results', 'History']

export default function Navbar({ activeTab, onTabChange }) {
  return (
    <nav style={styles.nav}>
      <div style={styles.logo}>
        Fit<span style={{ color: 'var(--accent)' }}>Mind</span> AI
      </div>
      <div style={styles.tabs}>
        {TABS.map(tab => (
          <button
            key={tab}
            style={{
              ...styles.tab,
              ...(activeTab === tab ? styles.tabActive : {}),
            }}
            onClick={() => onTabChange(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '20px 40px',
    borderBottom: '1px solid var(--border)',
    position: 'sticky',
    top: 0,
    background: 'rgba(11,15,26,0.85)',
    backdropFilter: 'blur(20px)',
    zIndex: 100,
  },
  logo: {
    fontFamily: 'Syne, sans-serif',
    fontWeight: 800,
    fontSize: '1.4rem',
    color: 'var(--text)',
  },
  tabs: {
    display: 'flex',
    gap: 4,
    background: 'var(--surface)',
    borderRadius: 12,
    padding: 4,
  },
  tab: {
    padding: '8px 18px',
    borderRadius: 9,
    fontSize: '0.85rem',
    fontWeight: 500,
    color: 'var(--muted)',
    border: 'none',
    background: 'none',
    transition: 'all 0.2s',
  },
  tabActive: {
    background: 'var(--accent)',
    color: '#000',
    fontWeight: 700,
  },
}
