export type MapType = 'dark' | 'light' | 'voyager' | 'satellite'

// ── Flight data (mirrors backend models/flight.py) ────────────────────────

export interface Flight {
  icao24: string
  callsign: string | null
  latitude: number | null
  longitude: number | null
  altitude: number | null
  velocity: number | null
  heading: number | null
}

export interface FlightResponse {
  count: number
  flights: Flight[]
}

// ── Airport ───────────────────────────────────────────────────────────────

export interface Airport {
  icao: string
  iata: string
  name: string
  city: string
  country: string
  lat: number
  lng: number
}
