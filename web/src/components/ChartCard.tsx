export default function ChartCard({ title, children }: { title: string; children: React.ReactNode }) { return <div className="card"><h3 className="mb-2">{title}</h3>{children}</div> }
