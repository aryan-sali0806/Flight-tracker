from fastapi import APIRouter, HTTPException

from models.flight import AircraftMeta, ErrorResponse
from services.aircraft_db import fetch_aircraft_meta, AircraftDBError

router = APIRouter()


@router.get(
    "/{icao24}",
    response_model=AircraftMeta,
    summary="Get static aircraft metadata",
    responses={
        401: {"model": ErrorResponse, "description": "OpenSky credentials not configured"},
        404: {"model": ErrorResponse, "description": "Aircraft not found in OpenSky database"},
        502: {"model": ErrorResponse, "description": "Aircraft database returned an error"},
        503: {"model": ErrorResponse, "description": "Aircraft database is unreachable"},
    },
)
async def get_aircraft_meta(icao24: str):
    """
    Fetch static metadata for an aircraft by its ICAO24 hex address.

    Returns registration (tail number), manufacturer, model, airline name,
    IATA/ICAO codes, build date, and engine type.

    Results are cached in memory — the first call fetches from OpenSky;
    every subsequent call for the same aircraft is instant.
    """
    try:
        return await fetch_aircraft_meta(icao24)
    except AircraftDBError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
