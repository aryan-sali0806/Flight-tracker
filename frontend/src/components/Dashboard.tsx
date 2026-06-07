interface Props {
  count: number
  lastUpdated: Date | null
}

export default function Dashboard({ count, lastUpdated }: Props) {
  const time = lastUpdated
    ? lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : '—'

  return (
    <div className="dashboard">
      <div className="dashboard-row">
        <span className="dashboard-label">Tracking</span>
        <span className="dashboard-value">{count} aircraft</span>
      </div>
      <div className="dashboard-row">
        <span className="dashboard-label">Updated</span>
        <span className="dashboard-value">{time}</span>
      </div>
    </div>
  )
}
