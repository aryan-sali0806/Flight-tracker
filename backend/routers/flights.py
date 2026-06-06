# Defines HTTP route handlers for flight-related endpoints.
# Calls the service layer; does not contain business logic.

import httpx
from fastapi import APIRouter, HTTPException
from models.flight import FlightResponse, ErrorResponse
from services.opensky import fetch_flights

# APIRouter is a mini-app you attach to the main FastAPI instance in main.py.
# Using routers keeps main.py clean and makes each feature independently testable.
router = APIRouter()


@router.get(
    "/",
    response_model=FlightResponse,
    summary="Get all live aircraft positions",
    responses={
        503: {"model": ErrorResponse, "description": "OpenSky API is unavailable"},
    },
)
async def get_flights():
    """
    Fetch current state vectors for all aircraft visible to the OpenSky Network.

    Returns a list of aircraft with their live positions, altitude, speed, and heading.
    Data is fetched directly from OpenSky on every request — no caching.
    """
    try:
        flights = await fetch_flights()
        return FlightResponse(count=len(flights), flights=flights)

    except httpx.TimeoutException:
        # OpenSky took too long to respond — tell the client to try again
        raise HTTPException(
            status_code=503,
            detail="OpenSky API timed out. Please try again shortly.",
        )

    except httpx.HTTPStatusError as exc:
        # OpenSky returned an error status (e.g. 429 rate limit, 500 server error)
        raise HTTPException(
            status_code=502,
            detail=f"OpenSky API returned an error: {exc.response.status_code}",
        )

    except httpx.RequestError:
        # Network-level failure — DNS failure, connection refused, etc.
        raise HTTPException(
            status_code=503,
            detail="Could not reach OpenSky API. Check your internet connection.",
        )
