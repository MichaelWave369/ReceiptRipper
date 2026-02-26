import { useEffect, useState } from 'react'
import { api } from '../api/client'
import EnvelopeCard from '../components/EnvelopeCard'
import Topbar from '../components/Topbar'

export default function Envelopes(){
  const [envelopes,setEnvelopes]=useState<any[]>([])
  const [summary,setSummary]=useState<any>({by_envelope:{}})
  useEffect(()=>{api('/api/envelopes').then(setEnvelopes);api('/api/reports/summary').then(setSummary)},[])
  return <div><Topbar title="Envelopes" /><div className="space-y-2">{envelopes.map(e=><EnvelopeCard key={e.id} e={e} spent={summary.by_envelope?.[e.name]||0} />)}</div></div>
}
