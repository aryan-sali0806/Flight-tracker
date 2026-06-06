# Application entry point.
# Creates the FastAPI instance, registers middleware, and mounts routers.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import flights
from config import APP_TITLE, APP_DESCRIPTION, APP_VERSION

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

# CORS allows the browser-based frontend (on a different port) to call this API.
# In production, replace "*" with your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Mount the flights router — all its routes will be prefixed with /flights
app.include_router(flights.router, prefix="/flights", tags=["Flights"])


@app.get("/health", tags=["Health"])
def health_check():
    """Returns 200 OK when the API is running."""
    return {"status": "ok"}
