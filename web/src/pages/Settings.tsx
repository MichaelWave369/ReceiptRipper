import { useEffect, useState } from 'react'
import { api } from '../api/client'
import Topbar from '../components/Topbar'

export default function Settings(){
  const [rates,setRates]=useState<any[]>([])
  const [payload,setPayload]=useState({base_currency:'USD',quote_currency:'EUR',rate:0.92,as_of_date:new Date().toISOString().slice(0,10),source:'manual'})
  useEffect(()=>{api('/api/fx/rates').then(setRates)},[])
  const addRate = async()=>{await api('/api/fx/rates',{method:'POST',body:JSON.stringify(payload)}); setRates(await api('/api/fx/rates'))}
  const wipe = async()=>{await api('/api/export/wipe',{method:'POST',body:JSON.stringify({confirm:'WIPE MY DATA'})}); alert('Wiped')}
  return <div className="space-y-3"><Topbar title="Settings" /><div className="card space-y-2"><h3>FX Rates</h3><input className="input" value={payload.base_currency} onChange={e=>setPayload({...payload,base_currency:e.target.value})}/><input className="input" value={payload.quote_currency} onChange={e=>setPayload({...payload,quote_currency:e.target.value})}/><input className="input" type="number" step="0.0001" value={payload.rate} onChange={e=>setPayload({...payload,rate:Number(e.target.value)})}/><button className="btn" onClick={addRate}>Save rate</button><div className="text-xs">{rates.length} rates stored</div></div><div className="card"><a href="/api/export/data.zip" className="btn-outline inline-block">Export data.zip</a><button className="btn ml-2" onClick={wipe}>Wipe data</button></div></div>
}
