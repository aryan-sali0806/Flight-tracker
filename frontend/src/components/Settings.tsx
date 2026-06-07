import { useState, useRef, useEffect } from 'react'
import type { MapType } from '../types'

const MAP_OPTIONS: { type: MapType; label: string; desc: string }[] = [
  { type: 'dark',      label: 'Dark',      desc: 'Aviation-style' },
  { type: 'light',     label: 'Light',     desc: 'Clean & minimal' },
  { type: 'voyager',   label: 'Street',    desc: 'Roads & labels' },
  { type: 'satellite', label: 'Satellite', desc: 'Esri imagery' },
]

interface Props {
  mapType: MapType
  onChange: (t: MapType) => void
}

export default function Settings({ mapType, onChange }: Props) {
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  return (
    <div ref={wrapperRef} className="settings-wrapper">
      <button
        className={`settings-btn${open ? ' active' : ''}`}
        onClick={() => setOpen(o => !o)}
        title="Map settings"
        aria-label="Open map settings"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
      </button>

      {open && (
        <div className="settings-panel">
          <p className="settings-title">Map Type</p>
          <div className="map-type-grid">
            {MAP_OPTIONS.map(opt => (
              <button
                key={opt.type}
                className={`map-type-btn${mapType === opt.type ? ' selected' : ''}`}
                onClick={() => { onChange(opt.type); setOpen(false) }}
              >
                <span className="map-type-label">{opt.label}</span>
                <span className="map-type-desc">{opt.desc}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
