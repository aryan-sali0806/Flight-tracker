import { useState, useRef, useEffect } from 'react'
import type { Airport } from '../types'
import { AIRPORTS } from '../data/airports'

interface Props {
  onSelectAirport: (airport: Airport) => void
}

export default function SearchBar({ onSelectAirport }: Props) {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Airport[]>([])
  const [open, setOpen] = useState(false)
  const wrapperRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const q = query.trim().toLowerCase()
    if (q.length < 2) {
      setResults([])
      setOpen(false)
      return
    }
    const matches = AIRPORTS.filter(a =>
      a.name.toLowerCase().includes(q) ||
      a.city.toLowerCase().includes(q) ||
      a.iata.toLowerCase().startsWith(q) ||
      a.icao.toLowerCase().startsWith(q)
    ).slice(0, 6)
    setResults(matches)
    setOpen(matches.length > 0)
  }, [query])

  // Close dropdown when clicking outside the search component
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleSelect = (airport: Airport) => {
    onSelectAirport(airport)
    setQuery(`${airport.iata} — ${airport.name}`)
    setOpen(false)
  }

  return (
    <div ref={wrapperRef} className="search-wrapper">
      <div className="search-input-row">
        <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          type="text"
          className="search-input"
          placeholder="Search airports, flights..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setOpen(true)}
        />
        {query && (
          <button
            className="search-clear"
            onMouseDown={e => { e.preventDefault(); setQuery(''); setOpen(false) }}
          >
            ×
          </button>
        )}
      </div>

      {open && (
        <ul className="search-dropdown">
          <li className="search-group-label">Airports</li>
          {results.map(airport => (
            <li
              key={airport.icao}
              className="search-result"
              onMouseDown={() => handleSelect(airport)}
            >
              <span className="result-code">{airport.iata}</span>
              <div className="result-text">
                <span className="result-name">{airport.name}</span>
                <span className="result-city">{airport.city}, {airport.country}</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
