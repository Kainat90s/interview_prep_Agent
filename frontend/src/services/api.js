import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function listSessions(){
  const res = await axios.get(`${API_BASE}/sessions/`)
  return res.data
}

export async function submitAnswer(payload){
  const res = await axios.post(`${API_BASE}/answers/`, payload)
  return res.data
}

export default { listSessions, submitAnswer }
