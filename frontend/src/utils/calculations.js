export function calculateBMI(weight, height) {
  const h = height / 100
  return (weight / (h * h)).toFixed(1)
}

export function getBMICategory(bmi) {
  if (bmi < 18.5) return 'Underweight'
  if (bmi < 25)   return 'Normal'
  if (bmi < 30)   return 'Overweight'
  return 'Obese'
}

/** Mifflin–St Jeor */
export function calculateBMR(weight, height, age, gender) {
  const base = 10 * weight + 6.25 * height - 5 * age
  return Math.round(gender === 'Female' ? base - 161 : base + 5)
}

export function getActivityMultiplier(activity) {
  const map = {
    'Sedentary':         1.2,
    'Lightly Active':    1.375,
    'Moderately Active': 1.55,
    'Very Active':       1.725,
    'Extremely Active':  1.9,
    'Athlete':           2.0,
  }
  return map[activity] || 1.55
}

export function calculateTDEE(bmr, activity) {
  return Math.round(bmr * getActivityMultiplier(activity))
}

export function formatDate(iso) {
  try {
    const d = new Date(iso)
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`
  } catch { return '' }
}
