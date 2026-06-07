import { useEffect } from 'react'
import { useMap } from 'react-leaflet'

export interface FlyTarget {
  coords: [number, number]
  zoom: number
}

interface Props {
  flyTarget: FlyTarget | null
}

export default function MapController({ flyTarget }: Props) {
  const map = useMap()

  useEffect(() => {
    if (flyTarget) {
      map.flyTo(flyTarget.coords, flyTarget.zoom, { duration: 1.5 })
    }
  }, [flyTarget, map])

  return null
}
