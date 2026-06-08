import type { FlightResponse, AircraftMeta } from '../types'
import type { RegionId } from '../data/regions'

const API_BASE = 'http://localhost:8000'

// _region is accepted but not yet sent — the backend does not yet support
// a ?region= query param. When it does, replace the fetch URL with:
//   `${API_BASE}/flights?region=${_region}`
export async function fetchFlights(_region?: RegionId): Promise<FlightResponse> {
  const response = await fetch(`${API_BASE}/flights`)

  if (!response.ok) {
    throw new Error(`Failed to fetch flights: ${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<FlightResponse>
}

export async function fetchAircraftMeta(icao24: string): Promise<AircraftMeta> {
  const response = await fetch(`${API_BASE}/aircraft/${icao24.toLowerCase()}`)

  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail ?? `Aircraft metadata error: ${response.status}`)
  }

  return response.json() as Promise<AircraftMeta>
}
