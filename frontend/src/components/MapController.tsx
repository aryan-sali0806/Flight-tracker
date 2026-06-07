import { useEffect } from 'react'
import { useMap } from 'react-leaflet'

interface Props {
  flyTarget: [number, number] | null
}

export default function MapController({ flyTarget }: Props) {
  const map = useMap()

  useEffect(() => {
    if (flyTarget) {
      map.flyTo(flyTarget, 12, { duration: 1.5 })
    }
  }, [flyTarget, map])

  return null
}
