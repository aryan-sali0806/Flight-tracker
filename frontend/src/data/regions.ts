export type RegionId = 'india' | 'europe' | 'north_america' | 'global'

export interface Region {
  id: RegionId
  label: string
  center: [number, number]
  zoom: number
  // Mirrors backend models/bbox.py constants.
  // Passed to fetchFlights() today (unused); becomes a real query param
  // once the backend supports GET /flights?region=<id>.
  bbox: { lamin: number; lamax: number; lomin: number; lomax: number } | null
}

export const REGIONS: Region[] = [
  {
    id: 'india',
    label: 'India',
    center: [22.5, 82.5],
    zoom: 5,
    bbox: { lamin: 6.5, lamax: 37.1, lomin: 68.1, lomax: 97.4 },
  },
  {
    id: 'europe',
    label: 'Europe',
    center: [54, 15],
    zoom: 4,
    bbox: { lamin: 36, lamax: 72, lomin: -10, lomax: 40 },
  },
  {
    id: 'north_america',
    label: 'North America',
    center: [45, -100],
    zoom: 4,
    bbox: { lamin: 15, lamax: 72, lomin: -168, lomax: -52 },
  },
  {
    id: 'global',
    label: 'Global',
    center: [20, 0],
    zoom: 2,
    bbox: null,
  },
]
