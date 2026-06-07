import { useState, useEffect } from 'react'
import Map from './components/Map'
import SearchBar from './components/SearchBar'
import Settings from './components/Settings'
import { fetchFlights } from './api/flights'
import type { MapType, Airport, Flight } from './types'

export default function App() {
  const [mapType, setMapType] = useState<MapType>('dark')
  const [flyTarget, setFlyTarget] = useState<[number, number] | null>(null)
  const [flights, setFlights] = useState<Flight[]>([])

  useEffect(() => {
    fetchFlights()
      .then(data => {
        console.log(`Received ${data.count} flights:`, data.flights)
        setFlights(data.flights)
      })
      .catch(err => {
        console.error('Could not fetch flights:', err)
      })
  }, [])

  const handleSelectAirport = (airport: Airport) => {
    setFlyTarget([airport.lat, airport.lng])
  }

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Map mapType={mapType} flyTarget={flyTarget} flights={flights} />

      <div className="top-bar">
        <SearchBar onSelectAirport={handleSelectAirport} />
        <Settings mapType={mapType} onChange={setMapType} />
      </div>
    </div>
  )
}
