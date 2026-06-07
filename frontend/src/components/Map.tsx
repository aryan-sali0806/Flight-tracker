import { MapContainer, TileLayer } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import type { MapType, Flight } from '../types'
import MapController from './MapController'
import FlightMarker from './FlightMarker'

const TILE_LAYERS: Record<MapType, {
  url: string
  attribution: string
  subdomains: string[]
}> = {
  dark: {
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: ['a', 'b', 'c', 'd'],
  },
  light: {
    url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: ['a', 'b', 'c', 'd'],
  },
  voyager: {
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: ['a', 'b', 'c', 'd'],
  },
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri — Source: Esri, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    subdomains: [],
  },
}

// Type predicate: narrows Flight to only those with confirmed coordinates.
// Using this in .filter() gives TypeScript a non-null latitude and longitude
// in the resulting array — no need for ! assertions inside .map().
function hasCoordinates(
  f: Flight
): f is Flight & { latitude: number; longitude: number } {
  return f.latitude !== null && f.longitude !== null
}

interface Props {
  mapType: MapType
  flyTarget: [number, number] | null
  flights: Flight[]
}

export default function Map({ mapType, flyTarget, flights }: Props) {
  const layer = TILE_LAYERS[mapType]
  const placedFlights = flights.filter(hasCoordinates)

  return (
    <MapContainer
      center={[20, 0]}
      zoom={2}
      minZoom={2}
      style={{ width: '100%', height: '100%' }}
    >
      <TileLayer
        key={mapType}
        url={layer.url}
        attribution={layer.attribution}
        subdomains={layer.subdomains}
      />
      <MapController flyTarget={flyTarget} />
      {placedFlights.map(flight => (
        <FlightMarker key={flight.icao24} flight={flight} />
      ))}
    </MapContainer>
  )
}
