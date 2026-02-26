import { Link, Outlet } from 'react-router-dom'
import BottomNav from './BottomNav'

export default function Layout() {
  return <div className="max-w-3xl mx-auto min-h-screen pb-24 px-3">
    <header className="py-4 flex justify-between items-center"><Link to="/" className="text-xl font-bold">ReceiptRipper</Link><Link className="btn" to="/scan">+ Add</Link></header>
    <Outlet />
    <BottomNav />
  </div>
}
