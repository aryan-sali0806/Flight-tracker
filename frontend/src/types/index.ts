export type MapType = 'dark' | 'light' | 'voyager' | 'satellite'

export interface Airport {
  icao: string
  iata: string
  name: string
  city: string
  country: string
  lat: number
  lng: number
}
