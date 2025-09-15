import React, { useEffect, useState } from 'react'
import { api } from '../api'
import { Link } from 'react-router-dom'

export default function Groups(){
  const [groups, setGroups] = useState([])
  const [form, setForm] = useState({ name:'' })
  const [err, setErr] = useState('')
  const reload = () => api.groups().then(setGroups).catch(()=>setGroups([]))
  useEffect(()=>{ reload() }, [])
  const create = async (e)=>{
    e.preventDefault(); setErr('')
    try{ await api.createGroup(form); setForm({name:''}); reload() }catch(e){ setErr(e.message) }
  }
  return (
    <div className="container grid cols-2">
      <div className="card">
        <h2 className="section-title">My Groups</h2>
        <div className="list">
          {groups.map(g=> (
            <div key={g.id} className="row" style={{justifyContent:'space-between'}}>
              <div><strong>{g.name}</strong></div>
              <Link className="link" to={`/groups/${g.id}`}>Open →</Link>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <h2 className="section-title">Create a Group</h2>
        <form className="stack" onSubmit={create}>
          <div className="stack"><label>Group name</label><input className="input" value={form.name} onChange={e=>setForm({name:e.target.value})} required /></div>
          {err && <div className="pill" style={{borderColor:'#ff4d4f', color:'#ffb3b3'}}>{err}</div>}
          <button className="btn">Create</button>
        </form>
      </div>
    </div>
  )
}
