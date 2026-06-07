import { useState } from 'react'
import Map from './components/Map'
import SearchBar from './components/SearchBar'
import Settings from './components/Settings'
import type { MapType, Airport } from './types'

export default function App() {
  const [mapType, setMapType] = useState<MapType>('dark')
  const [flyTarget, setFlyTarget] = useState<[number, number] | null>(null)

  const handleSelectAirport = (airport: Airport) => {
    setFlyTarget([airport.lat, airport.lng])
  }

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Map mapType={mapType} flyTarget={flyTarget} />

      <div className="top-bar">
        <SearchBar onSelectAirport={handleSelectAirport} />
        <Settings mapType={mapType} onChange={setMapType} />
      </div>
    </div>
  )
}
