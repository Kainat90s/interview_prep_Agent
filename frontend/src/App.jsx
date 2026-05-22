import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Interview from './pages/Interview'
import Result from './pages/Result'

export default function App(){
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/interview" element={<Interview/>} />
        <Route path="/result" element={<Result/>} />
      </Routes>
    </BrowserRouter>
  )
}
