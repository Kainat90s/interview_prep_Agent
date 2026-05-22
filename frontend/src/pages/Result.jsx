import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function Result() {
  const location = useLocation()
  
  // Use state passed from the interview screen, or default to 0 if directly accessed
  const scorecard = location.state?.score || 0
  const jobRole = location.state?.jobRole || 'General'
  const sessionId = location.state?.sessionId || null
  
  const normalizedScore = Math.min((scorecard / 5) * 100, 100)
  
  const getScoreInfo = (score) => {
    if (score >= 4) return { label: 'Excellent', color: '#34d399' }
    if (score >= 3) return { label: 'Good', color: '#fbbf24' }
    return { label: 'Needs Improvement', color: '#f87171' }
  }
  
  const info = getScoreInfo(scorecard)

  const handleDownload = async () => {
    if (!sessionId) {
      alert("No session ID found. Cannot download report.")
      return
    }
    
    try {
      const response = await fetch(`http://localhost:8000/api/download-report/${sessionId}`);
      if (!response.ok) throw new Error('Failed to download PDF');
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Interview_Report_${jobRole.replace(/\s+/g, '_')}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert('Failed to download report. Please try again.');
    }
  }

  return (
    <div className="page fade-in page-center">
      <div className="card result-page slide-up">
        <div style={{ fontSize: '4rem', marginBottom: '1rem', animation: 'slideUp 0.8s ease-out' }}>🏆</div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.5rem' }}>Interview Complete!</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
          Great job! Here is the overall evaluation of your performance for the <strong>{jobRole}</strong> role.
        </p>

        <div className="scorecard-wrapper">
          <div className="score-circle">
            <svg viewBox="0 0 36 36" style={{ width: '100%', height: '100%' }}>
              <defs>
                <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#6366f1" />
                  <stop offset="100%" stopColor="#a78bfa" />
                </linearGradient>
              </defs>
              <path
                className="circle-bg-track"
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <path
                className="circle-progress"
                strokeDasharray={`${normalizedScore}, 100`}
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
              />
              <text x="18" y="18" className="score-value" dy="0.3em">
                {scorecard.toFixed(1)}
              </text>
              <text x="18" y="24" className="score-unit">/ 5</text>
            </svg>
          </div>

          <div className="score-label-badge" style={{ color: info.color, borderColor: info.color }}>
            {info.label}
          </div>
          
          <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600, marginBottom: '2.5rem' }}>
            Overall Performance Score
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', maxWidth: '300px', margin: '0 auto' }}>
          <button className="btn btn-primary" onClick={handleDownload}>
            📄 Download Full PDF Report
          </button>
          <Link to="/" className="btn btn-secondary">
            Return Home
          </Link>
        </div>
      </div>
    </div>
  )
}
