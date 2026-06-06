# Pydantic models that define the shape of data flowing through the API.
# FastAPI uses these for automatic validation and JSON serialization.

from pydantic import BaseModel
from typing import Optional


class Flight(BaseModel):
    """Represents a single aircraft's current state vector from OpenSky."""

    icao24: str
    # ICAO 24-bit address — the unique hardware ID of the aircraft transponder

    callsign: Optional[str]
    # Flight callsign (e.g. "DLH2AB"). Can be None if the transponder isn't broadcasting it.

    latitude: Optional[float]
    # Decimal degrees. None means OpenSky received a signal but has no position fix yet.

    longitude: Optional[float]
    # Decimal degrees.

    altitude: Optional[float]
    # Barometric altitude in metres. None for ground vehicles or missing data.

    velocity: Optional[float]
    # Ground speed in metres per second.

    heading: Optional[float]
    # True track in degrees (0 = North, 90 = East). Not magnetic heading.


class FlightResponse(BaseModel):
    """Wrapper returned by GET /flights."""

    count: int
    # Total number of aircraft in this response

    flights: list[Flight]
    # The array of state vectors


class ErrorResponse(BaseModel):
    """Returned when something goes wrong (e.g. OpenSky is unreachable)."""

    detail: str
    # Human-readable description of what went wrong
