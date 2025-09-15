import React, { useEffect, useState } from 'react'
import { useAuth } from '../AuthContext'
import { api } from '../api'

export default function Courses(){
  const { user } = useAuth()
  const [courses, setCourses] = useState([])
  const [err, setErr] = useState('')
  const [form, setForm] = useState({ name:'', description:'' })
  const reload = () => api.courses().then(setCourses).catch(()=>setCourses([]))
  useEffect(()=>{ reload() }, [])

  const create = async (e)=>{
    e.preventDefault(); setErr('')
    try{ await api.createCourse(form); setForm({name:'', description:''}); reload() }
    catch(e){ setErr(e.message) }
  }
  const enroll = async (id)=>{
    try{ await api.enroll(id); alert('Enrolled'); } catch(e){ alert(e.message) }
  }

  return (
    <div className="container grid cols-2">
      <div className="card">
        <h2 className="section-title">All Courses</h2>
        <div className="list">
          {courses.map(c=>(
            <div key={c.id} className="card" style={{padding:'12px'}}>
              <div className="row" style={{justifyContent:'space-between'}}>
                <div>
                  <div><strong>{c.name}</strong></div>
                  <div className="muted">by {c.teacher?.display_name || c.teacher?.username}</div>
                </div>
                {user.role === 'student' && <button className="btn" onClick={()=>enroll(c.id)}>Enroll</button>}
              </div>
              <div className="muted" style={{marginTop:'8px'}}>{c.description}</div>
            </div>
          ))}
        </div>
      </div>
      {user.role === 'teacher' && (
        <div className="card">
          <h2 className="section-title">Create Course</h2>
          <form className="stack" onSubmit={create}>
            <div className="stack"><label>Name</label><input className="input" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} required /></div>
            <div className="stack"><label>Description</label><textarea className="input" value={form.description} onChange={e=>setForm({...form, description:e.target.value})}></textarea></div>
            {err && <div className="pill" style={{borderColor:'#ff4d4f', color:'#ffb3b3'}}>{err}</div>}
            <button className="btn">Create</button>
          </form>
        </div>
      )}
    </div>
  )
}
