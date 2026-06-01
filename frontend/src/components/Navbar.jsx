import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { BriefcaseIcon } from './Icons'

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="navbar animate-fadeIn">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <div className="navbar-logo-wrap">
            <BriefcaseIcon className="navbar-logo-icon" size={20} />
          </div>
          <span className="navbar-brand-name">AI Interview Prep</span>
        </Link>
        
        <div className="navbar-links">
          <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            Home
          </Link>
          <Link to="/interview" className={`nav-link ${location.pathname === '/interview' ? 'active' : ''}`}>
            Interview
          </Link>
          <Link to="/result" className={`nav-link ${location.pathname === '/result' ? 'active' : ''}`}>
            Results
          </Link>
        </div>
      </div>
    </nav>
  )
}
