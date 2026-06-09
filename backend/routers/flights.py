from fastapi import APIRouter, HTTPException, Query

from models.bbox import (
    BoundingBox,
    INDIA_BOUNDING_BOX,
    EUROPE_BOUNDING_BOX,
    NORTH_AMERICA_BOUNDING_BOX,
)
from models.flight import FlightResponse, ErrorResponse
from services.opensky import fetch_flights, OpenSkyError

router = APIRouter()

_REGION_BBOX: dict[str, BoundingBox | None] = {
    "india":         INDIA_BOUNDING_BOX,
    "europe":        EUROPE_BOUNDING_BOX,
    "north_america": NORTH_AMERICA_BOUNDING_BOX,
    "global":        None,
}


@router.get(
    "",
    response_model=FlightResponse,
    summary="Get all live aircraft positions",
    responses={
        400: {"model": ErrorResponse, "description": "Unknown region"},
        502: {"model": ErrorResponse, "description": "OpenSky returned an error"},
        503: {"model": ErrorResponse, "description": "OpenSky API is unreachable"},
    },
)
async def get_flights(
    region: str = Query("india", description="Region to fetch: india | europe | north_america | global"),
):
    """
    Fetch current state vectors for all aircraft in the requested region.

    Returns live position, altitude, speed, and heading for each aircraft.
    """
    if region not in _REGION_BBOX:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown region '{region}'. Valid values: {list(_REGION_BBOX)}",
        )

    try:
        flights = await fetch_flights(_REGION_BBOX[region])
        return FlightResponse(count=len(flights), flights=flights)

    except OpenSkyError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
