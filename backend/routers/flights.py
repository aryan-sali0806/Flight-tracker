from fastapi import APIRouter, HTTPException

from models.flight import FlightResponse, ErrorResponse
from services.opensky import fetch_flights, OpenSkyError

router = APIRouter()


@router.get(
    "/",
    response_model=FlightResponse,
    summary="Get all live aircraft positions",
    responses={
        502: {"model": ErrorResponse, "description": "OpenSky returned an error"},
        503: {"model": ErrorResponse, "description": "OpenSky API is unreachable"},
    },
)
async def get_flights():
    """
    Fetch current state vectors for all aircraft visible over India.

    Returns live position, altitude, speed, and heading for each aircraft.
    Data is fetched directly from OpenSky on every request.
    """
    try:
        flights = await fetch_flights()
        return FlightResponse(count=len(flights), flights=flights)

    except OpenSkyError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
