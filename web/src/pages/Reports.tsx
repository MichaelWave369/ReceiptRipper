import { useEffect, useState } from 'react'
import { Bar, BarChart, Pie, PieChart, ResponsiveContainer, Cell } from 'recharts'
import { api } from '../api/client'
import Topbar from '../components/Topbar'

export default function Reports(){
  const [summary,setSummary]=useState<any>({by_category:{}}); const [trend,setTrend]=useState<any[]>([])
  useEffect(()=>{api('/api/reports/summary').then(setSummary);api('/api/reports/trend').then(setTrend)},[])
  const pieData = Object.entries(summary.by_category||{}).map(([name,value])=>({name,value}))
  return <div className="space-y-3"><Topbar title="Reports" /><div className="card h-64"><ResponsiveContainer><PieChart><Pie data={pieData} dataKey="value" nameKey="name">{pieData.map((_,i)=><Cell key={i} fill={['#7c3aed','#06b6d4','#84cc16','#f59e0b'][i%4]} />)}</Pie></PieChart></ResponsiveContainer></div><div className="card h-64"><ResponsiveContainer><BarChart data={trend}><Bar dataKey="total_spent_cents" fill="#7c3aed"/></BarChart></ResponsiveContainer></div></div>
}
