import { NavLink } from 'react-router-dom'
const tabs = [['/','Dash'],['/transactions','Tx'],['/envelopes','Env'],['/reports','Rpt'],['/settings','Set']]
export default function BottomNav(){return <nav className="fixed bottom-0 left-0 right-0 bg-black/80 border-t border-white/10 p-2 flex justify-around">{tabs.map(([to,label])=><NavLink key={to} to={to} className="text-sm">{label}</NavLink>)}</nav>}
