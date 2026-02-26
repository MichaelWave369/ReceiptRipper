import { useEffect, useState } from 'react'
import { api } from '../api/client'
import Topbar from '../components/Topbar'

export default function Dashboard(){
  const [summary,setSummary]=useState<any>()
  useEffect(()=>{api('/api/reports/summary').then(setSummary)},[])
  return <div className="space-y-3"><Topbar title="Dashboard" />
    <div className="card">This month spent: {(summary?.total_spent_cents||0)/100} {summary?.currency||'USD'}</div>
    <div className="card">Top 3 categories: {Object.keys(summary?.by_category||{}).slice(0,3).join(', ')||'None'}</div>
    <div className="card">Envelopes at risk: {Object.entries(summary?.by_envelope||{}).filter(([,v]:any)=>v>0).length}</div>
  </div>
}
