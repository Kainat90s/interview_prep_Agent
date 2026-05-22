import React from 'react'
import { Link, useLocation } from 'react-router-dom'

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        <span className="navbar-brand-dot"></span>
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
    </nav>
  )
}
