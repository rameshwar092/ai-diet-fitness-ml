import React, { useState } from 'react'
import Navbar         from './components/Navbar'
import LoadingOverlay from './components/LoadingOverlay'
import ProfileForm    from './components/ProfileForm'
import ResultsPanel   from './components/ResultsPanel'
import HistoryPanel   from './components/HistoryPanel'
import { useHistory } from './hooks/useHistory'
import { fetchMLPlan, checkBackendHealth } from './utils/api'

export default function App() {
  const [activeTab, setActiveTab] = useState('Profile')
  const [loading,   setLoading]   = useState(false)
  const [plan,      setPlan]      = useState(null)
  const [error,     setError]     = useState('')

  const { history, saveToHistory, clearHistory } = useHistory()

  // ── Generate plan via ML backend ────────────────────────────
  async function handleGenerate(formData) {
    setError('')
    setLoading(true)

    // Check backend is alive
    const healthy = await checkBackendHealth()
    if (!healthy) {
      setLoading(false)
      setError('Unable to connect to the server. Please try again.')
      return
    }

    try {
      const result = await fetchMLPlan({
        name:            formData.name,
        age:             Number(formData.age),
        gender:          formData.gender,
        height:          Number(formData.height),
        weight:          Number(formData.weight),
        targetWeight:    formData.targetWeight ? Number(formData.targetWeight) : null,
        diets:           formData.diets,
        goal:            formData.goal,
        activity:        formData.activity,
        allergies:       formData.allergies,
        medical:         formData.medical,
        sleep:           formData.sleep,
        water:           formData.water,
        workoutDuration: formData.workoutDuration,
      })

      setPlan(result)
      setActiveTab('Results')
    } catch (err) {
      console.error(err)
      setError(err.message)
      alert('Error from ML backend: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleSave() {
    if (!plan) return
    saveToHistory(plan)
    alert('Plan saved to History!')
  }

  function handleLoadHistory(savedPlan) {
    setPlan(savedPlan)
    setActiveTab('Results')
  }

  return (
    <>
      <LoadingOverlay show={loading} />
      <Navbar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Error banner */}
      {error && (
        <div style={styles.errorBanner}>
            {error}
          <button style={styles.errorClose} onClick={() => setError('')}>✕</button>
        </div>
      )}

      {activeTab === 'Profile' && (
        <ProfileForm onSubmit={handleGenerate} loading={loading} />
      )}
      {activeTab === 'Results' && (
        <ResultsPanel
          plan={plan}
          onBack={() => setActiveTab('Profile')}
          onSave={handleSave}
        />
      )}
      {activeTab === 'History' && (
        <HistoryPanel
          history={history}
          onLoad={handleLoadHistory}
          onClear={() => { if (confirm('Clear all saved history?')) clearHistory() }}
        />
      )}
    </>
  )
}

const styles = {
  errorBanner: {
    background: 'rgba(255,107,53,0.15)',
    border: '1px solid rgba(255,107,53,0.4)',
    color: '#ff6b35',
    padding: '12px 20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    fontSize: '0.9rem',
    position: 'relative',
    zIndex: 10,
  },
  errorClose: {
    background: 'none',
    border: 'none',
    color: '#ff6b35',
    cursor: 'pointer',
    fontSize: '1rem',
    padding: '0 4px',
  },
}
