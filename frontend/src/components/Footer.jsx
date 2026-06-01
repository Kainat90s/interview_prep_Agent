import React from 'react'
import { Link } from 'react-router-dom'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-brand">
          <div className="footer-logo">
            <span className="logo-dot"></span>
            <span className="logo-text">AI Interview Prep</span>
          </div>
          <p className="footer-desc">
            An advanced AI-powered platform to help you practice job interviews, refine your answers, and build confidence.
          </p>
        </div>
        
        <div className="footer-links-group">
          <div className="footer-col">
            <h4>Platform</h4>
            <Link to="/">Home</Link>
            <Link to="/interview">Start Interview</Link>
            <Link to="/result">Past Results</Link>
          </div>
          
          <div className="footer-col">
            <h4>Guidelines</h4>
            <a href="#" onClick={(e) => e.preventDefault()}>STAR Method</a>
            <a href="#" onClick={(e) => e.preventDefault()}>Privacy Policy</a>
            <a href="#" onClick={(e) => e.preventDefault()}>Terms of Service</a>
          </div>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {currentYear} AI Interview Prep. All rights reserved.</p>
        <p className="footer-made">Made with ❤️ for career growth</p>
      </div>
    </footer>
  )
}
