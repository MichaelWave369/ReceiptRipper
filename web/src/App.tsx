import { Navigate, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import { useAuth } from './auth/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Scan from './pages/Scan'
import Transactions from './pages/Transactions'
import Envelopes from './pages/Envelopes'
import Reports from './pages/Reports'
import Settings from './pages/Settings'

export default function App(){
  const { token } = useAuth()
  if(!token) return <Login />
  return <Routes><Route path="/" element={<Layout />}><Route index element={<Dashboard/>}/><Route path="scan" element={<Scan/>}/><Route path="transactions" element={<Transactions/>}/><Route path="envelopes" element={<Envelopes/>}/><Route path="reports" element={<Reports/>}/><Route path="settings" element={<Settings/>}/><Route path="*" element={<Navigate to="/" />} /></Route></Routes>
}
