from dataclasses import dataclass


@dataclass(frozen=True)
class BoundingBox:
    """
    Geographic rectangle used to filter aircraft by region.
    frozen=True makes instances immutable — coordinates never change at runtime.
    """
    lamin: float  # southernmost latitude
    lamax: float  # northernmost latitude
    lomin: float  # westernmost longitude
    lomax: float  # easternmost longitude

    def to_params(self) -> dict[str, float]:
        """Returns query parameters the OpenSky API expects."""
        return {
            "lamin": self.lamin,
            "lamax": self.lamax,
            "lomin": self.lomin,
            "lomax": self.lomax,
        }


# --- Region definitions ---
# To add a new region: add one line here. Nothing else needs to change.

INDIA_BOUNDING_BOX = BoundingBox(
    lamin=6.5, lamax=37.1, lomin=68.1, lomax=97.4
)

EUROPE_BOUNDING_BOX = BoundingBox(
    lamin=36.0, lamax=71.0, lomin=-10.0, lomax=40.0
)

NORTH_AMERICA_BOUNDING_BOX = BoundingBox(
    lamin=15.0, lamax=72.0, lomin=-170.0, lomax=-50.0
)

MAHARASHTRA_BOUNDING_BOX = BoundingBox(
    lamin=15.6, lamax=22.1, lomin=72.6, lomax=80.9
)

PUNE_BOUNDING_BOX = BoundingBox(
    lamin=18.3, lamax=18.7, lomin=73.6, lomax=74.1
)
