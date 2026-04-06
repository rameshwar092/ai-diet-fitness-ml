// src/utils/api.js — calls the Python ML backend

const BASE_URL = 'http://localhost:8000'

/**
 * Send user profile to ML backend and get recommendation plan
 */
export async function fetchMLPlan(profileData) {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(profileData),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({}))
    
    const detail = Array.isArray(err.detail)
        ? err.detail.map(e => `${e.loc?.join('.')} — ${e.msg}`).join('; ')
        : err.detail || err.message || err.error || `Server error: ${response.status}`
    
    throw new Error(detail)
}

  return response.json()
}

/**
 * Health check — verify backend is running
 */
export async function checkBackendHealth() {
  try {
    const res = await fetch(`${BASE_URL}/health`, { signal: AbortSignal.timeout(3000) })
    return res.ok
  } catch {
    return false
  }
}
