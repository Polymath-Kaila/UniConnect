import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../api'

export default function GroupDetail(){
  const { id } = useParams()
  const [group, setGroup] = useState(null)
  const [users, setUsers] = useState([])
  const [projects, setProjects] = useState([])
  const [form, setForm] = useState({ name:'', description:'', repo_url:'' })
  const [inviteId, setInviteId] = useState('')

  const load = async ()=>{
    const [gr, us, pr] = await Promise.all([
      api.groups().then(arr=> arr.find(x=> String(x.id) === String(id))),
      api.users(''),
      api.projects()
    ])
    setGroup(gr || null)
    setUsers(us || [])
    setProjects((pr||[]).filter(p=> String(p.group?.id) === String(id)))
  }

  useEffect(()=>{ load() }, [id])

  const addMember = async ()=>{
    if(!inviteId) return
    await api.addMember(id, Number(inviteId))
    await load()
    setInviteId('')
  }

  const createProject = async (e)=>{
    e.preventDefault()
    await api.createProject({ group_id:Number(id), name:form.name, description:form.description, repo_url: form.repo_url })
    setForm({name:'', description:'', repo_url:''})
    await load()
  }

  if(!group) return <div className="container">Loading...</div>

  return (
    <div className="container grid cols-2">
      <div className="card">
        <h2 className="section-title">{group.name}</h2>
        <div className="stack">
          <div className="row">
            <select value={inviteId} onChange={e=>setInviteId(e.target.value)}>
              <option value="">Invite user...</option>
              {users.map(u => <option key={u.id} value={u.id}>{u.display_name || u.username}</option>)}
            </select>
            <button className="btn" onClick={addMember}>Add</button>
          </div>
        </div>
        <div className="spacer"></div>
        <h3 className="section-title">Projects</h3>
        <div className="list">
          {projects.map(p => (
            <div key={p.id} className="card" style={{padding:'12px'}}>
              <div><strong>{p.name}</strong></div>
              <div className="muted">{p.description}</div>
              {p.repo_url && <div style={{marginTop:'6px'}}><a className="link" href={p.repo_url} target="_blank" rel="noreferrer">Repo →</a></div>}
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <h3 className="section-title">Start a Project</h3>
        <form className="stack" onSubmit={createProject}>
          <div className="stack"><label>Name</label><input className="input" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} required /></div>
          <div className="stack"><label>Description</label><textarea className="input" value={form.description} onChange={e=>setForm({...form, description:e.target.value})}></textarea></div>
          <div className="stack"><label>Repository URL</label><input className="input" placeholder="https://github.com/..." value={form.repo_url} onChange={e=>setForm({...form, repo_url:e.target.value})} /></div>
          <button className="btn">Create</button>
        </form>
      </div>
    </div>
  )
}
