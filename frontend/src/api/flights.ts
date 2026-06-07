import type { FlightResponse } from '../types'

const API_BASE = 'http://localhost:8000'

export async function fetchFlights(): Promise<FlightResponse> {
  const response = await fetch(`${API_BASE}/flights`)

  if (!response.ok) {
    throw new Error(`Failed to fetch flights: ${response.status} ${response.statusText}`)
  }

  return response.json() as Promise<FlightResponse>
}
