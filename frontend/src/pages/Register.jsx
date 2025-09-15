import React, { useEffect, useState } from 'react'
import { api } from '../api'
import { Link, useNavigate } from 'react-router-dom'

export default function Register(){
  const nav = useNavigate()
  const [form, setForm] = useState({ role:'student' })
  const [universities, setUniversities] = useState([])
  const [err, setErr] = useState('')
  const [done, setDone] = useState(false)

  useEffect(()=>{ api.universities().then(setUniversities).catch(()=>setUniversities([])) }, [])
  const update = (k,v)=> setForm(prev=>({...prev, [k]:v}))

  const submit = async (e)=>{
    e.preventDefault(); setErr('')
    try {
      await api.register({
        username: form.username,
        email: form.email,
        password: form.password,
        display_name: form.display_name,
        role: form.role,
        university_id: Number(form.university_id),
        year_of_study: form.role==='student' ? Number(form.year_of_study||0) : undefined
      })
      setDone(true); setTimeout(()=>nav('/login'), 1200)
    } catch (e){ setErr(e.message) }
  }

  return (
    <div className="container grid cols-2">
      <div className="card">
        <h2 className="section-title">Create an account</h2>
        <form className="stack" onSubmit={submit}>
          <div className="stack"><label>Display name</label><input className="input" onChange={e=>update('display_name', e.target.value)} required /></div>
          <div className="grid cols-2">
            <div className="stack"><label>Username</label><input className="input" onChange={e=>update('username', e.target.value)} required /></div>
            <div className="stack"><label>Email</label><input className="input" type="email" onChange={e=>update('email', e.target.value)} required /></div>
          </div>
          <div className="grid cols-2">
            <div className="stack"><label>Password</label><input className="input" type="password" onChange={e=>update('password', e.target.value)} required /></div>
            <div className="stack"><label>Role</label>
              <select onChange={e=>update('role', e.target.value)} defaultValue="student">
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
              </select>
            </div>
          </div>
          <div className="grid cols-2">
            <div className="stack">
              <label>University</label>
              <select required onChange={e=>update('university_id', e.target.value)}>
                <option value="">-- Select your University --</option>
                {universities.length === 0
                  ? <option value=''>No universities found</option>
                  : universities.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}
              </select>
            </div>
            {form.role === 'student' && (
              <div className="stack"><label>Year of study</label><input className="input" onChange={e=>update('year_of_study', e.target.value)} /></div>
            )}
          </div>
          {err && <div className="pill" style={{borderColor:'#ff4d4f', color:'#ffb3b3'}}>{err}</div>}
          <button className="btn">Register</button>
        </form>
        {done && <div className="muted">🎉 Account created! Redirecting to login...</div>}
        <div className="spacer"></div>
        <div className="muted">Already have an account? <Link to="/login" className="link">Login</Link></div>
      </div>
      <div className="card">
        <h2 className="section-title">How mentors work</h2>
        <p className="muted">If you register as a <strong>student</strong>, we auto-assign you a teacher mentor (first from your university if available, else any teacher).</p>
      </div>
    </div>
  )
}
