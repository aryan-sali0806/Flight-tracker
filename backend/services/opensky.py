import logging
from typing import Any

import httpx

from config import (
    OPENSKY_STATES_ENDPOINT,
    OPENSKY_TIMEOUT_SECONDS,
    OPENSKY_USERNAME,
    OPENSKY_PASSWORD,
)
from models.bbox import BoundingBox, INDIA_BOUNDING_BOX
from models.flight import Flight

logger = logging.getLogger(__name__)


class OpenSkyError(Exception):
    """
    Raised when the OpenSky API is unreachable or returns an error.
    Carries an HTTP status code so the router can forward it to the client.
    """
    def __init__(self, detail: str, status_code: int = 503) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


# OpenSky returns each aircraft as a plain list, not a dict.
# These are the index positions of the fields we care about.
# Full reference: https://openskynetwork.github.io/opensky-api/rest.html
_ICAO24_IDX         = 0
_CALLSIGN_IDX       = 1
_ORIGIN_COUNTRY_IDX = 2   # country of registration
_LONGITUDE_IDX      = 5
_LATITUDE_IDX       = 6
_ALTITUDE_IDX       = 7   # baro_altitude in metres
_ON_GROUND_IDX      = 8   # boolean
_VELOCITY_IDX       = 9   # ground speed in m/s
_HEADING_IDX        = 10  # true track in degrees
_VERTICAL_RATE_IDX  = 11  # climb/descent rate in m/s
_SQUAWK_IDX         = 14  # 4-digit transponder code


def _parse_state_vector(state: list[Any]) -> Flight | None:
    """
    Convert a raw OpenSky state vector into a Flight model.
    Returns None if the entry is missing the ICAO24 identifier.
    """
    if not state or not state[_ICAO24_IDX]:
        return None

    raw_callsign = state[_CALLSIGN_IDX]
    callsign = raw_callsign.strip() if raw_callsign else None

    return Flight(
        icao24=state[_ICAO24_IDX],
        callsign=callsign or None,
        latitude=state[_LATITUDE_IDX],
        longitude=state[_LONGITUDE_IDX],
        altitude=state[_ALTITUDE_IDX],
        velocity=state[_VELOCITY_IDX],
        heading=state[_HEADING_IDX],
        on_ground=state[_ON_GROUND_IDX],
        vertical_rate=state[_VERTICAL_RATE_IDX],
        squawk=state[_SQUAWK_IDX] or None,
        origin_country=state[_ORIGIN_COUNTRY_IDX] or None,
    )


async def fetch_flights(bbox: BoundingBox | None = INDIA_BOUNDING_BOX) -> list[Flight]:
    """
    Fetch aircraft state vectors from OpenSky for the given bounding box.
    Pass None to fetch all flights globally (no geographic filter).

    Raises:
        OpenSkyError: for any failure communicating with the OpenSky API.
    """
    auth = (OPENSKY_USERNAME, OPENSKY_PASSWORD) if OPENSKY_USERNAME and OPENSKY_PASSWORD else None
    logger.info("Fetching flights for bbox: %s (auth=%s)", bbox, auth is not None)

    try:
        async with httpx.AsyncClient(timeout=OPENSKY_TIMEOUT_SECONDS) as client:
            response = await client.get(
                OPENSKY_STATES_ENDPOINT,
                params=bbox.to_params() if bbox is not None else {},
                auth=auth,
            )
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "unknown")
            logger.warning("OpenSky rate limit hit (Retry-After: %s)", retry_after)
            raise OpenSkyError(
                detail="OpenSky rate limit reached. Wait a moment and it will recover.",
                status_code=429,
            )
        response.raise_for_status()

    except httpx.TimeoutException:
        logger.error("OpenSky request timed out after %ds", OPENSKY_TIMEOUT_SECONDS)
        raise OpenSkyError(
            detail="OpenSky API timed out. Please try again shortly.",
            status_code=503,
        )

    except httpx.HTTPStatusError as exc:
        logger.error("OpenSky returned HTTP %d", exc.response.status_code)
        raise OpenSkyError(
            detail=f"OpenSky API returned an error: {exc.response.status_code}",
            status_code=502,
        )

    except httpx.RequestError as exc:
        logger.error("Network error reaching OpenSky: %s", exc)
        raise OpenSkyError(
            detail="Could not reach OpenSky API. Check your internet connection.",
            status_code=503,
        )

    data = response.json()
    raw_states: list[Any] = data.get("states") or []

    flights = [
        parsed
        for state in raw_states
        if (parsed := _parse_state_vector(state)) is not None
    ]

    logger.info("Returned %d aircraft", len(flights))
    return flights
