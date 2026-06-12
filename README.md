# Flight Tracker

A real-time aircraft tracking app powered by the [OpenSky Network](https://opensky-network.org). Watch live flights over India, Europe, North America, or the whole globe on an interactive map.

## Features

- Live aircraft positions refreshed every 10 seconds
- Interactive map with four tile styles: Dark, Light, Voyager, Satellite
- Click any aircraft to see a details card — callsign, altitude, speed, heading, vertical rate, and static metadata (manufacturer, model, registration, airline)
- Region selector: India, Europe, North America, Global
- Airport search — jump to any major airport instantly
- Server-side caching to minimize OpenSky API calls regardless of client count

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Python 3.12, FastAPI, httpx, Pydantic v2 |
| Frontend | React 19, TypeScript, Vite, Leaflet / react-leaflet |
| Data | OpenSky Network REST API |
| Package mgmt | uv (Python), npm (Node) |

## Project Structure

```
flight-tracker/
├── backend/
│   ├── main.py               # FastAPI app, CORS, logging
│   ├── config.py             # API URLs, credentials, cache TTL
│   ├── models/
│   │   ├── flight.py         # Flight, AircraftMeta, FlightResponse (Pydantic)
│   │   └── bbox.py           # BoundingBox dataclass + region constants
│   ├── routers/
│   │   ├── flights.py        # GET /flights
│   │   └── aircraft.py       # GET /aircraft/{icao24}
│   └── services/
│       ├── opensky.py        # OpenSky fetcher with TTL cache
│       └── aircraft_db.py    # Aircraft metadata fetcher with permanent cache
└── frontend/
    └── src/
        ├── App.tsx
        ├── api/flights.ts    # Typed API client
        ├── components/
        │   ├── Map.tsx
        │   ├── FlightMarker.tsx
        │   ├── AircraftCard.tsx
        │   ├── RegionSelector.tsx
        │   ├── SearchBar.tsx
        │   ├── Settings.tsx
        │   └── Dashboard.tsx
        ├── data/
        │   ├── regions.ts
        │   └── airports.ts
        └── types/index.ts
```

## Caching

The backend has two independent in-memory caches that eliminate redundant OpenSky requests.

### Flight state vector cache (TTL)

`services/opensky.py` keeps a per-region TTL cache keyed by bounding box. When multiple clients request the same region simultaneously, only the first request hits OpenSky — every subsequent one within the TTL window gets the cached result.

| Setting | Value | Location |
|---|---|---|
| TTL | 10 seconds | `config.py → FLIGHTS_CACHE_TTL_SECONDS` |
| Scope | Per region (India / Europe / North America / Global) | `_flight_cache` dict |

The 10-second TTL matches OpenSky's own state-vector update interval, so no live data is lost.

### Aircraft metadata cache (permanent)

`services/aircraft_db.py` caches aircraft registration, manufacturer, model, and airline data permanently for the lifetime of the server process. Aircraft metadata is static — an aircraft's ICAO24 address, registration, and type never change — so there is no reason to re-fetch it.

The first request for a given ICAO24 address hits the OpenSky Aircraft Database; every subsequent request for the same aircraft is served instantly from memory.

## Getting Started

### Prerequisites

- Python 3.12+ and [uv](https://github.com/astral-sh/uv)
- Node.js 18+ and npm

### 1. Backend

```bash
# From the project root
uv sync
cd backend
uvicorn main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the Swagger UI.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

### OpenSky credentials (optional)

The `/flights` endpoint works without an account. The aircraft metadata endpoint (`/aircraft/{icao24}`) requires a free OpenSky account for full access.

Create an account at [opensky-network.org](https://opensky-network.org), then set these environment variables before starting the backend:

```powershell
# Windows PowerShell
$env:OPENSKY_USERNAME = "your_username"
$env:OPENSKY_PASSWORD = "your_password"
```

```bash
# Linux / macOS
export OPENSKY_USERNAME=your_username
export OPENSKY_PASSWORD=your_password
```

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/flights?region=india` | Live aircraft state vectors for a region |
| GET | `/aircraft/{icao24}` | Static metadata for one aircraft |
| GET | `/docs` | Interactive Swagger UI |

Supported `region` values: `india`, `europe`, `north_america`, `global`.

## Data Source

Aircraft positions come from the [OpenSky Network](https://opensky-network.org), a non-profit community network of ADS-B receivers. Data is provided under the [OpenSky Network Terms of Use](https://opensky-network.org/about/terms-of-use).
