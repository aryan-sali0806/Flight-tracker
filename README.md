# Flight Tracker

A real-time aircraft tracking app powered by the [OpenSky Network](https://opensky-network.org). Watch live flights over India, Europe, North America, or the whole globe on an interactive map.

![Flight Tracker screenshot](frontend/src/assets/hero.png)

## Features

- Live aircraft positions refreshed every 10 seconds
- Interactive map with four tile styles: Dark, Light, Voyager, Satellite
- Click any aircraft to see a details card — callsign, altitude, speed, heading, vertical rate, and static metadata (manufacturer, model, registration, airline)
- Region selector to switch between India, Europe, North America, and Global views
- Airport search — jump to any major airport instantly

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
│   ├── config.py             # API URLs, credentials, app metadata
│   ├── models/
│   │   ├── flight.py         # Flight, AircraftMeta, FlightResponse (Pydantic)
│   │   └── bbox.py           # BoundingBox dataclass + region constants
│   ├── routers/
│   │   ├── flights.py        # GET /flights
│   │   └── aircraft.py       # GET /aircraft/{icao24}
│   └── services/
│       ├── opensky.py        # OpenSky state vector fetcher
│       └── aircraft_db.py    # Aircraft metadata fetcher (with in-memory cache)
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

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

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

```bash
# Windows PowerShell
$env:OPENSKY_USERNAME = "your_username"
$env:OPENSKY_PASSWORD = "your_password"
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/flights?region=india` | Live aircraft for a region |
| GET | `/aircraft/{icao24}` | Static metadata for one aircraft |
| GET | `/docs` | Swagger UI |

Supported `region` values: `india`, `europe`, `north_america`, `global`.

## Data Source

Aircraft positions come from the [OpenSky Network](https://opensky-network.org), a non-profit community network of ADS-B receivers. Data is provided under the [OpenSky Network Terms of Use](https://opensky-network.org/about/terms-of-use).
