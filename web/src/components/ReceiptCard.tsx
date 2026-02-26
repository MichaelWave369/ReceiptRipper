export default function ReceiptCard({ receipt }: { receipt: any }) { return <div className="card"><div>{receipt.filename}</div><div className="text-xs opacity-70">{receipt.mime}</div></div> }
