export default function TransactionForm({ draft, onChange }: { draft: any; onChange: (v: any) => void }) {
  return <div className="space-y-2">
    <input className="input" value={draft.merchant || ''} onChange={e => onChange({ ...draft, merchant: e.target.value })} placeholder="Merchant" />
    <input className="input" type="number" value={draft.amount_cents || 0} onChange={e => onChange({ ...draft, amount_cents: Number(e.target.value) })} placeholder="Amount cents" />
    <input className="input" value={draft.currency || 'USD'} onChange={e => onChange({ ...draft, currency: e.target.value.toUpperCase() })} placeholder="Currency" />
  </div>
}
