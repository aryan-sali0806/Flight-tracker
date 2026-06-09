import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from routers import flights, aircraft

# Configure once here — all loggers in every module inherit this automatically
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    redirect_slashes=False,
)

# CORS allows the browser-based frontend (on a different port) to call this API.
# In production, replace "*" with your actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(flights.router, prefix="/flights", tags=["Flights"])
app.include_router(aircraft.router, prefix="/aircraft", tags=["Aircraft"])


@app.get("/health", tags=["Health"])
def health_check():
    """Returns 200 OK when the API is running."""
    return {"status": "ok"}
