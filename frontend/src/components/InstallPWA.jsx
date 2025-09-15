import React, { useEffect, useState } from 'react'
export default function InstallPWA(){
  const [promptEvent, setPromptEvent] = useState(null)
  const [visible, setVisible] = useState(false)
  useEffect(()=>{
    const handler = (e)=>{ e.preventDefault(); setPromptEvent(e); setVisible(true) }
    window.addEventListener('beforeinstallprompt', handler)
    return ()=> window.removeEventListener('beforeinstallprompt', handler)
  },[])
  if(!visible) return null
  const install = async ()=>{
    if(!promptEvent) return
    promptEvent.prompt()
    await promptEvent.userChoice
    setVisible(false)
  }
  return <button className="btn" onClick={install}>Install App</button>
}
