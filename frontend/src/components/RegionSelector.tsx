import { REGIONS } from '../data/regions'
import type { RegionId } from '../data/regions'

interface Props {
  activeRegion: RegionId
  onChange: (id: RegionId) => void
}

export default function RegionSelector({ activeRegion, onChange }: Props) {
  return (
    <div className="region-selector">
      {REGIONS.map(region => (
        <button
          key={region.id}
          className={`region-btn${activeRegion === region.id ? ' active' : ''}`}
          onClick={() => onChange(region.id)}
        >
          {region.label}
        </button>
      ))}
    </div>
  )
}
