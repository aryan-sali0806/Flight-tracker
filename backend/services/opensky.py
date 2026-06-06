# Handles all communication with the OpenSky Network API.
# The router calls fetch_flights() and gets back clean Flight objects.
# Raw API details are fully contained here.

import httpx
from typing import Optional
from models.flight import Flight
from config import OPENSKY_STATES_ENDPOINT, OPENSKY_TIMEOUT_SECONDS, BoundingBox, INDIA_BOUNDING_BOX


# OpenSky returns each aircraft as a plain list (not a dict).
# These are the index positions of the fields we care about.
# Full field reference: https://openskynetwork.github.io/opensky-api/rest.html
_ICAO24_IDX    = 0
_CALLSIGN_IDX  = 1
_LATITUDE_IDX  = 6
_LONGITUDE_IDX = 5
_ALTITUDE_IDX  = 7   # baro_altitude (metres)
_VELOCITY_IDX  = 9   # velocity (m/s)
_HEADING_IDX   = 10  # true_track (degrees)


def _parse_state_vector(state: list) -> Optional[Flight]:
    """
    Convert a raw OpenSky state vector (a list) into a Flight model.
    Returns None if the entry is malformed or missing the ICAO24 identifier.
    """
    if not state or not state[_ICAO24_IDX]:
        # Skip entries that have no aircraft identifier — unusable data
        return None

    # Callsign comes with trailing spaces from OpenSky — strip them
    raw_callsign = state[_CALLSIGN_IDX]
    callsign = raw_callsign.strip() if raw_callsign else None

    return Flight(
        icao24=state[_ICAO24_IDX],
        callsign=callsign or None,   # convert empty string to None
        latitude=state[_LATITUDE_IDX],
        longitude=state[_LONGITUDE_IDX],
        altitude=state[_ALTITUDE_IDX],
        velocity=state[_VELOCITY_IDX],
        heading=state[_HEADING_IDX],
    )


async def fetch_flights(bbox: BoundingBox = INDIA_BOUNDING_BOX) -> list[Flight]:
    """
    Fetch aircraft state vectors from OpenSky for the given bounding box.
    Defaults to Indian airspace if no region is specified.

    Raises:
        httpx.TimeoutException: if OpenSky does not respond in time
        httpx.HTTPStatusError: if OpenSky returns a non-2xx status
        httpx.RequestError: for any other network-level failure
    """
    # async with creates a fresh HTTP client for this request and closes it cleanly afterwards
    async with httpx.AsyncClient(timeout=OPENSKY_TIMEOUT_SECONDS) as client:
        response = await client.get(
            OPENSKY_STATES_ENDPOINT,
            params=bbox.to_params(),
        )

        # Raise an exception immediately if OpenSky returned 4xx or 5xx
        response.raise_for_status()

        data = response.json()

        # OpenSky returns {"time": ..., "states": [[...], [...]]}
        # "states" is None when no aircraft are visible (rare but possible)
        raw_states = data.get("states") or []

        # Parse each state vector, dropping any that fail validation
        flights = [
            parsed
            for state in raw_states
            if (parsed := _parse_state_vector(state)) is not None
        ]

        return flights
