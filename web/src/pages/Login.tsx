import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import { useAuth } from '../auth/AuthContext'

export default function Login(){
  const { login } = useAuth(); const nav = useNavigate();
  const [email,setEmail]=useState('demo@example.com'); const [password,setPassword]=useState('password123');
  const submit = async () => { await api('/api/auth/register',{method:'POST',body:JSON.stringify({email,password,default_currency:'USD'})}).catch(()=>{}); await login(email,password); nav('/') }
  return <div className="max-w-sm mx-auto mt-20 card space-y-3"><h1 className="text-2xl">Login</h1><input className="input" value={email} onChange={e=>setEmail(e.target.value)} /><input className="input" type="password" value={password} onChange={e=>setPassword(e.target.value)} /><button className="btn w-full" onClick={submit}>Continue</button></div>
}
