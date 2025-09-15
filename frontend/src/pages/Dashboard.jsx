import React, { useEffect, useState } from 'react'
import { useAuth } from '../AuthContext'
import { api } from '../api'

export default function Dashboard(){
  const { user } = useAuth()
  const [enrollments, setEnrollments] = useState([])
  const [groups, setGroups] = useState([])
  useEffect(()=>{
    api.enrollments().then(setEnrollments).catch(()=>setEnrollments([]))
    api.groups().then(setGroups).catch(()=>setGroups([]))
  }, [])
  return (
    <div className="container grid cols-3">
      <div className="card">
        <h3 className="section-title">Welcome, {user.display_name || user.username}</h3>
        <p className="muted">Role: {user.role}</p>
        {user.role === 'student' && (
          <p className="muted">Mentor: {user.mentor ? user.mentor.display_name : 'Not yet assigned'}</p>
        )}
      </div>
      <div className="card">
        <h3 className="section-title">My Courses</h3>
        <div className="list">
          {enrollments.length === 0 && <div className="muted">No enrollments yet.</div>}
          {enrollments.map(e=> (
            <div key={e.id} className="card" style={{padding:'12px'}}>
              <div className="row" style={{justifyContent:'space-between'}}>
                <div>
                  <div><strong>{e.course.name}</strong></div>
                  <div className="muted">{e.course.teacher?.display_name}</div>
                </div>
                <span className="pill">{e.status}</span>
              </div>
              <div className='muted' style={{fontSize:'12px', marginTop:'8px'}}>Progress</div>
              <div style={{width:'100%', height:'10px', background:'#222', borderRadius:'999px', overflow:'hidden', border:'1px solid var(--border)'}}>
                <div style={{width:`${e.progress||0}%`, height:'100%', background:'linear-gradient(90deg,#ff7a00,#7c3aed)'}}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="card">
        <h3 className="section-title">My Groups</h3>
        <div className="list">
          {groups.length === 0 && <div className="muted">No groups yet.</div>}
          {groups.map(g=> (
            <div key={g.id} className="row" style={{justifyContent:'space-between'}}>
              <div><strong>{g.name}</strong></div>
              <a className="link" href={`/groups/${g.id}`}>Open →</a>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
