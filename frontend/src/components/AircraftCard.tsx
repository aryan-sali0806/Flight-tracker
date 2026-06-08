import { useEffect, useState } from 'react'
import type { Flight, AircraftMeta } from '../types'
import { fetchAircraftMeta } from '../api/flights'

interface Props {
  flight: Flight
  onClose: () => void
}

function fmtAlt(m: number | null): string {
  if (m === null) return '—'
  return `${Math.round(m * 3.281).toLocaleString()} ft`
}

function fmtSpeed(mps: number | null): string {
  if (mps === null) return '—'
  return `${Math.round(mps * 1.944)} kts`
}

function fmtHeading(deg: number | null): string {
  if (deg === null) return '—'
  return `${Math.round(deg)}°`
}

function fmtVerticalRate(mps: number | null): string {
  if (mps === null) return '—'
  const fpm = Math.round(mps * 196.85)
  return `${fpm >= 0 ? '↑' : '↓'} ${Math.abs(fpm).toLocaleString()} fpm`
}

function Row({ label, value, valueClass }: { label: string; value: string; valueClass?: string }) {
  return (
    <div className="ac-row">
      <span className="ac-label">{label}</span>
      <span className={`ac-value${valueClass ? ` ${valueClass}` : ''}`}>{value}</span>
    </div>
  )
}

export default function AircraftCard({ flight, onClose }: Props) {
  const [meta, setMeta] = useState<AircraftMeta | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setMeta(null)
    setLoading(true)
    setError(null)

    fetchAircraftMeta(flight.icao24)
      .then(data => { setMeta(data); setLoading(false) })
      .catch(err => { setError(err.message ?? 'Metadata unavailable'); setLoading(false) })
  }, [flight.icao24])

  const aircraftLabel = [meta?.manufacturer, meta?.model].filter(Boolean).join(' ')

  const vrFpm = flight.vertical_rate !== null ? Math.round(flight.vertical_rate * 196.85) : null
  const vrClass = vrFpm === null ? undefined : vrFpm >= 0 ? 'ac-vrate-up' : 'ac-vrate-down'

  const statusClass = flight.on_ground === null
    ? undefined
    : flight.on_ground ? 'ac-status-badge ac-status-ground' : 'ac-status-badge ac-status-airborne'
  const statusText = flight.on_ground === null
    ? null
    : flight.on_ground ? 'On Ground' : 'Airborne'

  return (
    <div className="aircraft-card">

      {/* Header */}
      <div className="ac-header">
        <div className="ac-header-left">
          <span className="ac-callsign">{flight.callsign?.trim() || 'Unknown'}</span>
          <div className="ac-airline-row">
            <span className="ac-airline">{meta?.airline_name ?? ' '}</span>
            {statusClass && statusText && (
              <span className={statusClass}>{statusText}</span>
            )}
          </div>
        </div>
        <button className="ac-close" onClick={onClose} aria-label="Close">×</button>
      </div>

      {/* Model + registration */}
      {(aircraftLabel || meta?.registration) && (
        <div className="ac-identity">
          {aircraftLabel}
          {meta?.registration && <span className="ac-reg"> · {meta.registration}</span>}
        </div>
      )}

      {/* Live data */}
      <div className="ac-section-label ac-section-live">Live</div>
      <div className="ac-rows">
        <Row label="Altitude"      value={fmtAlt(flight.altitude)} />
        <Row label="Speed"         value={fmtSpeed(flight.velocity)} />
        <Row label="Heading"       value={fmtHeading(flight.heading)} />
        {flight.vertical_rate !== null && (
          <Row label="Vertical rate" value={fmtVerticalRate(flight.vertical_rate)} valueClass={vrClass} />
        )}
        {flight.squawk && <Row label="Squawk" value={flight.squawk} />}
      </div>

      {/* Static metadata */}
      <div className="ac-section-label ac-section-aircraft">Aircraft</div>
      {loading && <div className="ac-loading">Loading metadata</div>}
      {error && !loading && <div className="ac-error">{error}</div>}
      {meta && (
        <div className="ac-rows">
          {meta.typecode && <Row label="Type"    value={meta.typecode} />}
          {meta.built    && <Row label="Built"   value={meta.built} />}
          {meta.engines  && <Row label="Engines" value={meta.engines} />}
          {meta.owner && meta.owner !== meta.airline_name && (
            <Row label="Owner" value={meta.owner} />
          )}
          {meta.airline_iata && <Row label="IATA" value={meta.airline_iata} />}
          {meta.airline_icao && <Row label="ICAO" value={meta.airline_icao} />}
        </div>
      )}

      {/* Footer */}
      <div className="ac-footer">
        <span className="ac-icao">{flight.icao24.toUpperCase()}</span>
        {flight.origin_country && <span className="ac-country">{flight.origin_country}</span>}
      </div>

    </div>
  )
}
