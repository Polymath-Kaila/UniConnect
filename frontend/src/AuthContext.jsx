import React, { createContext, useContext, useState, useEffect } from 'react'
import { api, setToken as saveToken, clearToken as wipe } from './api'
const Ctx = createContext(null)
export const useAuth = () => useContext(Ctx)

export default function AuthProvider({children}){
  const [token, setToken] = useState(localStorage.getItem('token')||'')
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  useEffect(()=>{
    if(token){
      saveToken(token)
      api.me().then(setUser).catch(()=>{ setToken(''); wipe(); }).finally(()=>setLoading(false))
    }else setLoading(false)
  }, [token])
  const login = async (username, password) => {
    const data = await api.login(username, password)
    const t = data.access; setToken(t); saveToken(t)
    const me = await api.me(); setUser(me)
  }
  const logout = () => { setUser(null); setToken(''); wipe(); }
  return <Ctx.Provider value={{token, user, loading, login, logout, setUser}}>{children}</Ctx.Provider>
}
