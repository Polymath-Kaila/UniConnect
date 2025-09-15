import React, { useState } from 'react'
import { useAuth } from '../AuthContext'
import { useNavigate, Link } from 'react-router-dom'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [err, setErr] = useState('')
  const { login } = useAuth()
  const nav = useNavigate()
  const submit = async (e)=>{
    e.preventDefault(); setErr('')
    try { await login(username, password); nav('/') } catch (e) { setErr(e.message) }
  }
  return (
    <div className="container grid cols-2">
      <div className="card">
        <h2 className="section-title">Welcome back</h2>
        <p className="muted">Sign in to continue</p>
        <div className="spacer"></div>
        <form className="stack" onSubmit={submit}>
          <div className="stack"><label>Username</label><input className="input" value={username} onChange={e=>setUsername(e.target.value)} /></div>
          <div className="stack"><label>Password</label><input type="password" className="input" value={password} onChange={e=>setPassword(e.target.value)} /></div>
          {err && <div className="pill" style={{borderColor:'#ff4d4f', color:'#ffb3b3'}}>{err}</div>}
          <button className="btn">Login</button>
        </form>
        <div className="spacer"></div>
        <div className="muted">No account? <Link to="/register" className="link">Register</Link></div>
      </div>
      <div className="card">
        <h2 className="section-title">Why UniConnect?</h2>
        <p className="muted">Enroll in teacher-led courses, get an auto-assigned mentor, form groups, and ship projects together.</p>
      </div>
    </div>
  )
}
