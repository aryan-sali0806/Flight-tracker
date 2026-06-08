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
  on_ground: boolean | null
  vertical_rate: number | null
  squawk: string | null
  origin_country: string | null
}

export interface AircraftMeta {
  icao24: string
  registration: string | null
  manufacturer: string | null
  model: string | null
  typecode: string | null
  airline_name: string | null
  airline_icao: string | null
  airline_iata: string | null
  owner: string | null
  built: string | null
  engines: string | null
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
