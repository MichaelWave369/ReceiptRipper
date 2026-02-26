import { useEffect, useState } from 'react'
import { api } from '../api/client'
import Topbar from '../components/Topbar'

export default function Transactions(){
  const [txs,setTxs]=useState<any[]>([])
  useEffect(()=>{api('/api/transactions').then(setTxs)},[])
  return <div><Topbar title="Transactions" /><div className="space-y-2">{txs.map(t=><div className="card" key={t.id}>{t.merchant||'Unknown'} - {t.amount_cents/100} {t.currency}</div>)}</div></div>
}
