import { useState } from 'react'

const HISTORY_KEY = 'fitmind_history'
const MAX_HISTORY = 10

export function useHistory() {
  const load = () => JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]')

  const [history, setHistory] = useState(load)

  function saveToHistory(plan) {
    const updated = [{ ...plan, savedAt: new Date().toISOString() }, ...load()]
    if (updated.length > MAX_HISTORY) updated.pop()
    localStorage.setItem(HISTORY_KEY, JSON.stringify(updated))
    setHistory(updated)
  }

  function clearHistory() {
    localStorage.removeItem(HISTORY_KEY)
    setHistory([])
  }

  return { history, saveToHistory, clearHistory }
}