import { useState } from 'react'
import { api } from '../api/client'
import Topbar from '../components/Topbar'
import TransactionForm from '../components/TransactionForm'

export default function Scan(){
  const [file,setFile]=useState<File|null>(null); const [draft,setDraft]=useState<any>(); const [ocr,setOcr]=useState('')
  const upload = async ()=>{if(!file) return; const fd=new FormData(); fd.append('file',file); const r=await fetch('/api/receipts/upload',{method:'POST',headers:{Authorization:`Bearer ${localStorage.getItem('token')||''}`},body:fd}); const j=await r.json(); setDraft(j.transaction_draft); setOcr(j.receipt.ocr_text)}
  const save = async ()=>{ await api('/api/transactions',{method:'POST',body:JSON.stringify(draft)}); alert('Saved') }
  return <div className="space-y-3"><Topbar title="Scan Receipt" /><input className="input" type="file" accept="image/*" capture="environment" onChange={e=>setFile(e.target.files?.[0]||null)} /><button className="btn" onClick={upload}>Upload & OCR</button>{draft&&<><TransactionForm draft={draft} onChange={setDraft}/><button className="btn-outline" onClick={save}>Save transaction</button></>}<pre className="card text-xs max-h-40 overflow-auto">{ocr||'OCR text appears here'}</pre></div>
}
