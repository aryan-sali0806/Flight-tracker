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
    on_ground: bool | None = Field(
        None, description="True if the aircraft is on the ground (taxiing), False if airborne."
    )
    vertical_rate: float | None = Field(
        None, description="Climb/descent rate in m/s. Positive = climbing, negative = descending."
    )
    squawk: str | None = Field(
        None, description="4-digit transponder squawk code."
    )
    origin_country: str | None = Field(
        None, description="Country of registration, inferred from the ICAO24 address prefix."
    )


class AircraftMeta(BaseModel):
    """Static metadata for an aircraft from the OpenSky Aircraft Database."""

    icao24: str = Field(..., description="ICAO 24-bit address used to look up this record")
    registration: str | None = Field(None, description="Tail number, e.g. 'VT-ANB'")
    manufacturer: str | None = Field(None, description="Airframe manufacturer, e.g. 'Boeing'")
    model: str | None = Field(None, description="Aircraft model, e.g. '737-800'")
    typecode: str | None = Field(None, description="ICAO type designator, e.g. 'B738'")
    airline_name: str | None = Field(None, description="Operating airline, e.g. 'Air India'")
    airline_icao: str | None = Field(None, description="3-letter ICAO airline code, e.g. 'AIC'")
    airline_iata: str | None = Field(None, description="2-letter IATA airline code, e.g. 'AI'")
    owner: str | None = Field(None, description="Legal owner — may differ from operator for leased aircraft")
    built: str | None = Field(None, description="Delivery/build date, e.g. '2019-04-12'")
    engines: str | None = Field(None, description="Engine type, e.g. 'CFM56-7B27'")


class FlightResponse(BaseModel):
    """Wrapper returned by GET /flights."""

    count: int = Field(..., description="Total number of aircraft in this response")
    flights: list[Flight] = Field(..., description="Array of aircraft state vectors")


class ErrorResponse(BaseModel):
    """Returned when something goes wrong (e.g. OpenSky is unreachable)."""

    detail: str = Field(..., description="Human-readable description of what went wrong")
