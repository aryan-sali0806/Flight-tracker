# All application-level configuration lives here.
# Import from this module instead of hardcoding values elsewhere.

# Base URL for the OpenSky Network REST API (no authentication required for public data)
OPENSKY_API_URL = "https://opensky-network.org/api"

# Endpoint that returns all current aircraft state vectors
OPENSKY_STATES_ENDPOINT = f"{OPENSKY_API_URL}/states/all"

# How long (seconds) to wait for OpenSky to respond before giving up
OPENSKY_TIMEOUT_SECONDS = 10

# App metadata shown in the auto-generated /docs page
APP_TITLE = "Flight Tracker API"
APP_DESCRIPTION = "Real-time aircraft positions powered by the OpenSky Network"
APP_VERSION = "1.0.0"
