import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { 
  BriefcaseIcon, 
  PaperclipIcon, 
  DocumentIcon, 
  CheckIcon, 
  BulbIcon, 
  SendIcon, 
  SpinnerIcon, 
  RocketIcon 
} from '../components/Icons'

// Use the deployed API base URL if available, otherwise fallback to localhost
const API_BASE_URL = (import.meta.env.VITE_API_BASE || 'http://localhost:8000') + '/api'

export default function Interview() {
  const navigate = useNavigate()
  
  // Setup state
  const [jobRole, setJobRole] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [resume, setResume] = useState(null)
  
  // Session state
  const [sessionStarted, setSessionStarted] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Chat state
  const [messages, setMessages] = useState([])
  const [currentInput, setCurrentInput] = useState('')
  const [currentQuestionData, setCurrentQuestionData] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleStart = async (e) => {
    e.preventDefault()
    if (!jobRole.trim()) return
    setLoading(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('job_role', jobRole)
      formData.append('job_description', jobDescription)
      if (resume) {
        formData.append('resume', resume)
      }

      const response = await fetch(`${API_BASE_URL}/start-session`, {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Failed to start session. Backend might be down.')
      }
      
      const data = await response.json()
      setSessionId(data.session_id)
      setCurrentQuestionData(data.first_question)
      
      setMessages([
        {
          id: `q-${data.first_question.question_number}`,
          type: 'bot',
          text: data.first_question.question,
          isQuestion: true
        }
      ])
      
      setSessionStarted(true)
    } catch (err) {
      setError(err.message || 'Something went wrong.')
    } finally {
      setLoading(false)
    }
  }

  const handleAnswerSubmit = async (e) => {
    e.preventDefault()
    if (!currentInput.trim() || loading) return

    const userAnswer = currentInput
    setCurrentInput('')
    
    const newUserMsg = {
      id: `a-${currentQuestionData.question_number}`,
      type: 'user',
      text: userAnswer
    }
    
    setMessages(prev => [...prev, newUserMsg])
    setLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/submit-answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          question_number: currentQuestionData.question_number,
          user_answer: userAnswer
        })
      })

      if (!response.ok) throw new Error('Failed to submit answer')
      
      const data = await response.json()
      
      const feedbackMsg = {
        id: `f-${currentQuestionData.question_number}`,
        type: 'feedback',
        evaluation: data.evaluation
      }
      
      setMessages(prev => [...prev, feedbackMsg])

      if (data.next_question) {
        setTimeout(() => {
          setMessages(prev => [...prev, {
            id: `q-${data.next_question.question_number}`,
            type: 'bot',
            text: data.next_question.question,
            isQuestion: true
          }])
          setCurrentQuestionData(data.next_question)
          setLoading(false)
        }, 1000)
      } else {
        setTimeout(() => {
          navigate('/result', { state: { score: data.overall_session_score, sessionId: sessionId, jobRole: jobRole } })
        }, 2000)
      }
      
    } catch (err) {
      console.error(err)
      setLoading(false)
    }
  }

  const getScoreStyle = (score) => {
    if (score >= 4) return { color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.2)', background: 'rgba(16, 185, 129, 0.05)' }
    if (score >= 3) return { color: '#f59e0b', borderColor: 'rgba(245, 158, 11, 0.2)', background: 'rgba(245, 158, 11, 0.05)' }
    return { color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.2)', background: 'rgba(239, 68, 68, 0.05)' }
  }

  return (
    <div className="page fade-in page-center" style={sessionStarted ? { padding: '1rem' } : {}}>
      <div className={sessionStarted ? "chat-container" : "card slide-up"} style={sessionStarted ? { maxWidth: '860px', width: '100%', height: 'calc(100vh - 180px)' } : { maxWidth: '600px', width: '100%' }}>
        
        {!sessionStarted ? (
          <div>
            <h1 style={{ fontSize: '1.8rem', marginBottom: '0.5rem', fontWeight: 800 }}>Start Interview Session</h1>
            <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
              Configure your interview parameters to begin.
            </p>
            
            {error && <div className="error-box"><span>⚠️</span> {error}</div>}
            
            <form onSubmit={handleStart}>
              <div className="form-group">
                <label className="form-label" htmlFor="jobRole">Job Role Target <span style={{color: 'red'}}>*</span></label>
                <input 
                  type="text" 
                  id="jobRole"
                  className="form-input"
                  placeholder="e.g. Backend Engineer, Data Scientist"
                  value={jobRole}
                  onChange={(e) => setJobRole(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label" htmlFor="jobDescription">Job Description (Optional)</label>
                <textarea 
                  id="jobDescription"
                  className="form-textarea"
                  rows="3"
                  placeholder="Paste job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                />
              </div>
              
              <div className="form-group">
                <label className="form-label" htmlFor="resume">Resume (Optional)</label>
                <div className={`upload-zone ${resume ? 'has-file' : ''}`}>
                  <input 
                    type="file" 
                    id="resume" 
                    accept=".pdf,.docx" 
                    onChange={(e) => setResume(e.target.files[0])}
                  />
                  {resume ? (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
                      <PaperclipIcon size={20} style={{ color: 'var(--success)' }} />
                      <span style={{ fontWeight: 650, color: 'var(--success)' }}>{resume.name}</span>
                    </div>
                  ) : (
                    <div style={{ color: 'var(--text-muted)' }}>
                      <DocumentIcon className="upload-zone-icon" size={32} style={{ display: 'block', margin: '0 auto 0.75rem' }} />
                      <strong>Click to upload</strong> or drag and drop<br/>
                      <small>PDF or DOCX</small>
                    </div>
                  )}
                </div>
              </div>
              
              <button type="submit" className="btn btn-primary" disabled={loading} style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem', alignItems: 'center', justifyContent: 'center' }}>
                {loading ? (
                  <>
                    <SpinnerIcon size={18} />
                    Generating 10 Questions...
                  </>
                ) : (
                  <>
                    <RocketIcon size={18} />
                    Launch Interview
                  </>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }} className="slide-up">
            <div className="chat-header">
              <div className="role-badge">
                <BriefcaseIcon size={15} />
                {jobRole}
              </div>
              <div className="question-counter">
                Q{currentQuestionData?.question_number || 1} / 10
              </div>
            </div>
            
            <div className="chat-messages">
              {messages.map((msg) => (
                <div key={msg.id} className={`message-wrapper ${msg.type}`}>
                  {msg.type === 'bot' && (
                    <div className="message bot-message slide-right">
                      <div className="avatar">AI</div>
                      <div className="bubble">{msg.text}</div>
                    </div>
                  )}
                  
                  {msg.type === 'user' && (
                    <div className="message user-message slide-left">
                      <div className="bubble">{msg.text}</div>
                    </div>
                  )}
                  
                  {msg.type === 'feedback' && (
                    <div className="feedback-card scale-in">
                      <h4>
                        <CheckIcon size={16} />
                        Feedback
                      </h4>
                      <div className="scores-row">
                        <div className="score-badge" style={getScoreStyle(msg.evaluation.clarity_score)}>
                          Clarity: {msg.evaluation.clarity_score}/5
                        </div>
                        <div className="score-badge" style={getScoreStyle(msg.evaluation.relevance_score)}>
                          Relevance: {msg.evaluation.relevance_score}/5
                        </div>
                        <div className="score-badge" style={getScoreStyle(msg.evaluation.star_score)}>
                          STAR: {msg.evaluation.star_score}/5
                        </div>
                      </div>
                      <p className="tip">
                        <BulbIcon className="tip-icon" size={18} />
                        {msg.evaluation.feedback}
                      </p>
                    </div>
                  )}
                </div>
              ))}
              {loading && (
                <div className="message bot-message slide-right">
                  <div className="avatar">AI</div>
                  <div className="typing-indicator">
                    <span></span><span></span><span></span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
            
            <form className="chat-input-area" onSubmit={handleAnswerSubmit}>
              <textarea
                value={currentInput}
                onChange={(e) => setCurrentInput(e.target.value)}
                placeholder="Type your answer here..."
                disabled={loading}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleAnswerSubmit(e);
                  }
                }}
              />
              <button type="submit" disabled={!currentInput.trim() || loading} className="send-btn">
                {loading ? <SpinnerIcon size={18} /> : <SendIcon size={18} />}
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  )
}
