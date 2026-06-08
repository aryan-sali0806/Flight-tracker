import logging
from typing import Any

import httpx

from config import (
    OPENSKY_AIRCRAFT_ENDPOINT,
    OPENSKY_TIMEOUT_SECONDS,
    OPENSKY_USERNAME,
    OPENSKY_PASSWORD,
)
from models.flight import AircraftMeta

logger = logging.getLogger(__name__)

# Permanent in-memory cache — aircraft registration and model never change.
# Key: lowercase icao24 hex string. Value: parsed AircraftMeta.
_cache: dict[str, AircraftMeta] = {}


class AircraftDBError(Exception):
    """Raised when the OpenSky Aircraft Database is unreachable or returns an error."""

    def __init__(self, detail: str, status_code: int = 503) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def _coerce(value: Any) -> str | None:
    """Return None for missing or blank values; strip whitespace from strings."""
    if value is None:
        return None
    s = str(value).strip()
    return s or None


async def fetch_aircraft_meta(icao24: str) -> AircraftMeta:
    """
    Return metadata for an aircraft by its ICAO24 hex address.

    Results are cached permanently — the first call hits the OpenSky Aircraft
    Database; every subsequent call for the same icao24 is served from memory.

    Raises:
        AircraftDBError: for 401/403 (missing credentials), 404 (unknown aircraft),
                         timeout, or any other network failure.
    """
    icao24 = icao24.lower().strip()

    if icao24 in _cache:
        logger.debug("Aircraft DB cache hit: %s", icao24)
        return _cache[icao24]

    auth = (OPENSKY_USERNAME, OPENSKY_PASSWORD) if OPENSKY_USERNAME and OPENSKY_PASSWORD else None

    logger.info("Fetching aircraft metadata for %s (auth=%s)", icao24, auth is not None)

    try:
        async with httpx.AsyncClient(timeout=OPENSKY_TIMEOUT_SECONDS) as client:
            response = await client.get(
                f"{OPENSKY_AIRCRAFT_ENDPOINT}/{icao24}",
                auth=auth,
            )

        if response.status_code == 404:
            raise AircraftDBError(
                detail=f"No metadata found for aircraft {icao24.upper()}",
                status_code=404,
            )
        if response.status_code in (401, 403):
            raise AircraftDBError(
                detail=(
                    "OpenSky Aircraft Database requires authentication. "
                    "Set OPENSKY_USERNAME and OPENSKY_PASSWORD environment variables."
                ),
                status_code=401,
            )

        response.raise_for_status()

    except httpx.TimeoutException:
        logger.error("Aircraft DB request timed out for %s", icao24)
        raise AircraftDBError(
            detail="OpenSky Aircraft Database timed out. Try again shortly.",
            status_code=503,
        )
    except httpx.HTTPStatusError as exc:
        logger.error("Aircraft DB returned HTTP %d for %s", exc.response.status_code, icao24)
        raise AircraftDBError(
            detail=f"OpenSky Aircraft Database returned an error: {exc.response.status_code}",
            status_code=502,
        )
    except httpx.RequestError as exc:
        logger.error("Network error reaching Aircraft DB: %s", exc)
        raise AircraftDBError(
            detail="Could not reach OpenSky Aircraft Database. Check your connection.",
            status_code=503,
        )

    data: dict = response.json()

    meta = AircraftMeta(
        icao24=icao24,
        registration=_coerce(data.get("registration")),
        manufacturer=_coerce(data.get("manufacturerName")),
        model=_coerce(data.get("model")),
        typecode=_coerce(data.get("typecode")),
        airline_name=_coerce(data.get("operator")),
        airline_icao=_coerce(data.get("operatorIcao")),
        airline_iata=_coerce(data.get("operatorIata")),
        owner=_coerce(data.get("owner")),
        built=_coerce(data.get("built")),
        engines=_coerce(data.get("engines")),
    )

    _cache[icao24] = meta
    logger.info(
        "Cached metadata for %s: %s %s operated by %s",
        icao24,
        meta.manufacturer,
        meta.model,
        meta.airline_name,
    )
    return meta
