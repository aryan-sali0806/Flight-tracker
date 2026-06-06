# All application-level configuration lives here.
# Import from this module instead of hardcoding values elsewhere.

from dataclasses import dataclass

# Base URL for the OpenSky Network REST API (no authentication required for public data)
OPENSKY_API_URL = "https://opensky-network.org/api"

# Endpoint that returns all current aircraft state vectors
OPENSKY_STATES_ENDPOINT = f"{OPENSKY_API_URL}/states/all"

# How long (seconds) to wait for OpenSky to respond before giving up
OPENSKY_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class BoundingBox:
    """
    Geographic rectangle used to filter aircraft by region.
    Pass any instance to fetch_flights() to switch regions without
    touching the API calling logic.
    frozen=True makes instances immutable — coordinates should never change at runtime.
    """
    lamin: float  # southernmost latitude
    lamax: float  # northernmost latitude
    lomin: float  # westernmost longitude
    lomax: float  # easternmost longitude

    def to_params(self) -> dict:
        """Returns the dict httpx needs as query parameters for the OpenSky API."""
        return {
            "lamin": self.lamin,
            "lamax": self.lamax,
            "lomin": self.lomin,
            "lomax": self.lomax,
        }


# --- Region definitions ---
# To add a new region: add one line here. Nothing else needs to change.

INDIA_BOUNDING_BOX = BoundingBox(
    lamin=6.5, lamax=37.1, lomin=68.1, lomax=97.4
)

EUROPE_BOUNDING_BOX = BoundingBox(
    lamin=36.0, lamax=71.0, lomin=-10.0, lomax=40.0
)

NORTH_AMERICA_BOUNDING_BOX = BoundingBox(
    lamin=15.0, lamax=72.0, lomin=-170.0, lomax=-50.0
)

MAHARASHTRA_BOUNDING_BOX = BoundingBox(
    lamin=15.6, lamax=22.1, lomin=72.6, lomax=80.9
)

PUNE_BOUNDING_BOX = BoundingBox(
    lamin=18.3, lamax=18.7, lomin=73.6, lomax=74.1
)


# App metadata shown in the auto-generated /docs page
APP_TITLE = "Flight Tracker API"
APP_DESCRIPTION = "Real-time aircraft positions powered by the OpenSky Network"
APP_VERSION = "1.0.0"
