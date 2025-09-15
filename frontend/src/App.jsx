import React from 'react'
import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom'
import AuthProvider, { useAuth } from './AuthContext'
import InstallPWA from './components/InstallPWA'
import Footer from './components/Footer'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Courses from './pages/Courses'
import Groups from './pages/Groups'
import GroupDetail from './pages/GroupDetail'

const Nav = () => {
  const { user, logout } = useAuth()
  const nav = useNavigate()
  return (
    <div className="nav">
      <div className="nav-inner">
        <Link to="/" className="brand">Uni<strong>Connect</strong></Link>
        <div className="row" style={{gap: '16px'}}>
          <Link to="/courses">Courses</Link>
          <Link to="/groups">Groups</Link>
          <InstallPWA />
          {user ? (
            <>
              <span className="pill">{user.display_name || user.username} • {user.role}</span>
              <button className="btn outline" onClick={()=>{logout(); nav('/login')}}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/register" className="btn">Register</Link>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

const Protected = ({children}) => {
  const { user, loading } = useAuth()
  if(loading) return <div className="container">Loading...</div>
  if(!user) return <Navigate to="/login" replace />
  return children
}

export default function App(){
  return (
    <AuthProvider>
      <Nav />
      <Routes>
        <Route path="/" element={<Protected><Dashboard /></Protected>} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/courses" element={<Protected><Courses /></Protected>} />
        <Route path="/groups" element={<Protected><Groups /></Protected>} />
        <Route path="/groups/:id" element={<Protected><GroupDetail /></Protected>} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
      <Footer />
    </AuthProvider>
  )
}
