# All application-level configuration lives here.
# Import from this module instead of hardcoding values elsewhere.

import os

# Base URL for the OpenSky Network REST API (no authentication required for public data)
OPENSKY_API_URL = "https://opensky-network.org/api"

# Endpoint that returns all current aircraft state vectors
OPENSKY_STATES_ENDPOINT = f"{OPENSKY_API_URL}/states/all"

# Endpoint for the aircraft metadata database (requires auth — set env vars below)
OPENSKY_AIRCRAFT_ENDPOINT = f"{OPENSKY_API_URL}/metadata/aircraft/icao"

# How long (seconds) to wait for OpenSky to respond before giving up
OPENSKY_TIMEOUT_SECONDS = 10

# How long (seconds) to serve cached flight data before hitting OpenSky again.
# OpenSky updates state vectors every ~10s; caching for the same duration means
# at most one outbound request per region per interval regardless of client count.
FLIGHTS_CACHE_TTL_SECONDS = 10

# Optional credentials for authenticated OpenSky access.
# The aircraft metadata endpoint requires these. Create a free account at
# https://opensky-network.org and set these env vars before starting the server.
OPENSKY_USERNAME: str | None = os.getenv("OPENSKY_USERNAME")
OPENSKY_PASSWORD: str | None = os.getenv("OPENSKY_PASSWORD")

# App metadata shown in the auto-generated /docs page
APP_TITLE = "Flight Tracker API"
APP_DESCRIPTION = "Real-time aircraft positions powered by the OpenSky Network"
APP_VERSION = "1.0.0"
