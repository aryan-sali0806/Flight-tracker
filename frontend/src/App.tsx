import { useState, useEffect } from 'react'
import Map from './components/Map'
import SearchBar from './components/SearchBar'
import Settings from './components/Settings'
import Dashboard from './components/Dashboard'
import RegionSelector from './components/RegionSelector'
import AircraftCard from './components/AircraftCard'
import { fetchFlights } from './api/flights'
import { REGIONS } from './data/regions'
import type { RegionId } from './data/regions'
import type { FlyTarget } from './components/MapController'
import type { MapType, Airport, Flight } from './types'

export default function App() {
  const [mapType, setMapType] = useState<MapType>('dark')
  const [flyTarget, setFlyTarget] = useState<FlyTarget | null>(null)
  const [flights, setFlights] = useState<Flight[]>([])
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)
  const [activeRegion, setActiveRegion] = useState<RegionId>('india')
  const [selectedFlight, setSelectedFlight] = useState<Flight | null>(null)

  useEffect(() => {
    const load = () =>
      fetchFlights(activeRegion)
        .then(data => {
          setFlights(data.flights)
          setLastUpdated(new Date())
        })
        .catch(err => console.error('Could not fetch flights:', err))

    load()
    const intervalId = setInterval(load, 10_000)
    return () => clearInterval(intervalId)
  }, [activeRegion])

  const handleRegionChange = (id: RegionId) => {
    const region = REGIONS.find(r => r.id === id)!
    setActiveRegion(id)
    setFlyTarget({ coords: region.center, zoom: region.zoom })
  }

  const handleSelectAirport = (airport: Airport) => {
    setFlyTarget({ coords: [airport.lat, airport.lng], zoom: 12 })
  }

  return (
    <div style={{ width: '100vw', height: '100vh', position: 'relative' }}>
      <Map mapType={mapType} flyTarget={flyTarget} flights={flights} onFlightClick={setSelectedFlight} />

      <div className="top-bar">
        <div className="top-bar-controls">
          <SearchBar onSelectAirport={handleSelectAirport} />
          <Settings mapType={mapType} onChange={setMapType} />
        </div>
        <RegionSelector activeRegion={activeRegion} onChange={handleRegionChange} />
      </div>

      <Dashboard count={flights.length} lastUpdated={lastUpdated} />

      {selectedFlight && (
        <AircraftCard flight={selectedFlight} onClose={() => setSelectedFlight(null)} />
      )}
    </div>
  )
}
