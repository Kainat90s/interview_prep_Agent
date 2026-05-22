import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listSessions } from '../services/api'

export default function Home() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listSessions()
      .then(data => {
        setSessions(data.sessions || [])
        setLoading(false)
      })
      .catch(err => {
        console.error("Failed to load sessions:", err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="page fade-in">
      <section className="home-hero">
        <div className="home-hero-badge">✨ AI-Powered Preparation</div>
        <h1>Ace Your Next <span>Tech Interview</span></h1>
        <p>
          Practice with our intelligent AI interviewer. Get tailored questions based on your target role and resume, with detailed feedback on every answer.
        </p>
        <Link to="/interview" className="home-cta-btn">
          Start New Interview
        </Link>

        <div className="home-features">
          <div className="feature-card">
            <div className="feature-icon">🎯</div>
            <h3>Role Specific</h3>
            <p>Questions tailored exactly to the job description and title you are targeting.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🧠</div>
            <h3>AI Feedback</h3>
            <p>Real-time analysis on clarity, relevance, and the STAR method.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <h3>Resume Context</h3>
            <p>The AI reviews your resume to ask personalized follow-up questions.</p>
          </div>
        </div>
      </section>

      <section className="sessions-section">
        <h2>Past Interview Sessions</h2>
        {loading ? (
          <div className="sessions-empty">Loading your sessions...</div>
        ) : sessions.length > 0 ? (
          <ul className="sessions-list">
            {sessions.map((s, i) => (
              <li key={i} className="session-item">
                <strong>Session ID:</strong> {s.id} | <strong>Role:</strong> {s.job_role || 'General'}
              </li>
            ))}
          </ul>
        ) : (
          <div className="sessions-empty">
            No previous sessions found. Start a new interview to see your history here!
          </div>
        )}
      </section>
    </div>
  )
}
