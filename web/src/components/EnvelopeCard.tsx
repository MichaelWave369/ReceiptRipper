export default function EnvelopeCard({ e, spent }: { e: any; spent: number }) {
  const pct = Math.min(100, Math.round((spent / e.monthly_budget_cents) * 100 || 0))
  return <div className="card"><div className="flex justify-between"><span>{e.name}</span><span>{pct}%</span></div><div className="h-2 bg-white/10 rounded mt-2"><div className="h-2 bg-neon rounded" style={{ width: `${pct}%` }} /></div></div>
}
