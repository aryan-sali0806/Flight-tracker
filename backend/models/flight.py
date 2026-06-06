from pydantic import BaseModel, Field


class Flight(BaseModel):
    """Represents a single aircraft's current state vector from OpenSky."""

    icao24: str = Field(
        ..., description="ICAO 24-bit address — unique hardware ID of the aircraft transponder"
    )
    callsign: str | None = Field(
        None, description="Flight callsign (e.g. 'DLH2AB'). None if the transponder isn't broadcasting it."
    )
    latitude: float | None = Field(
        None, description="Decimal degrees. None means no position fix yet."
    )
    longitude: float | None = Field(
        None, description="Decimal degrees."
    )
    altitude: float | None = Field(
        None, description="Barometric altitude in metres."
    )
    velocity: float | None = Field(
        None, description="Ground speed in metres per second."
    )
    heading: float | None = Field(
        None, description="True track in degrees (0=North, 90=East)."
    )


class FlightResponse(BaseModel):
    """Wrapper returned by GET /flights."""

    count: int = Field(..., description="Total number of aircraft in this response")
    flights: list[Flight] = Field(..., description="Array of aircraft state vectors")


class ErrorResponse(BaseModel):
    """Returned when something goes wrong (e.g. OpenSky is unreachable)."""

    detail: str = Field(..., description="Human-readable description of what went wrong")
