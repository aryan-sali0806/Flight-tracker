import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import type { Flight } from '../types'

// Build a rotated SVG plane icon for one aircraft.
// L.divIcon renders arbitrary HTML — no image file needed.
// The outer div applies the CSS rotation so the plane nose points
// in the direction of travel (heading 0 = north = up on the map).
function createPlaneIcon(heading: number | null): L.DivIcon {
  const deg = heading ?? 0
  return L.divIcon({
    className: '',
    html: `
      <div style="
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        transform: rotate(${deg}deg);
      ">
        <svg viewBox="0 0 24 24" width="22" height="22" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M12 2 L8.5 9 L2 11 L8.5 13 L7 22 L12 19.5 L17 22 L15.5 13 L22 11 L15.5 9 Z"
            fill="#60a5fa"
            stroke="#0f172a"
            stroke-width="0.8"
            stroke-linejoin="round"
          />
        </svg>
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -16],
  })
}

function formatAltitude(metres: number | null): string {
  if (metres === null) return '—'
  return `${Math.round(metres * 3.281).toLocaleString()} ft`
}

function formatSpeed(mps: number | null): string {
  if (mps === null) return '—'
  return `${Math.round(mps * 1.944)} kts`
}

function formatHeading(deg: number | null): string {
  if (deg === null) return '—'
  return `${Math.round(deg)}°`
}

interface Props {
  flight: Flight & { latitude: number; longitude: number }
}

export default function FlightMarker({ flight }: Props) {
  const icon = createPlaneIcon(flight.heading)

  return (
    <Marker position={[flight.latitude, flight.longitude]} icon={icon}>
      <Popup>
        <div className="flight-popup">
          <div className="popup-callsign">
            {flight.callsign?.trim() || 'Unknown'}
          </div>
          <div className="popup-rows">
            <div className="popup-row">
              <span className="popup-label">Altitude</span>
              <span className="popup-value">{formatAltitude(flight.altitude)}</span>
            </div>
            <div className="popup-row">
              <span className="popup-label">Speed</span>
              <span className="popup-value">{formatSpeed(flight.velocity)}</span>
            </div>
            <div className="popup-row">
              <span className="popup-label">Heading</span>
              <span className="popup-value">{formatHeading(flight.heading)}</span>
            </div>
          </div>
          <div className="popup-icao">{flight.icao24.toUpperCase()}</div>
        </div>
      </Popup>
    </Marker>
  )
}
