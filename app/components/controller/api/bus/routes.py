# DEPENDENCIES
## Third-Party
from fastapi import APIRouter
## Local
from constants.api import VONE_API_ROUTE
from constants.layer import LayerKeys, LayerActions
from constants.queue import BusKeys, BusSources, BusDirections
from .models import PostBusMessage, VerifyResponse
from .service import bus_publish


# CONSTANTS
VONE_CHAT_ROUTE: str = f"{VONE_API_ROUTE}/bus"


# API
router = APIRouter(
    prefix=VONE_CHAT_ROUTE,
    tags=["bus"],
    responses={404: {"description": "Not found"}}
)


# BUS
def _bus_publish(direction: str, payload: dict[str, str]) -> dict[str, str]:
    bus_publish(bus_direction=direction, payload=payload)

    response: dict[str, str] = {
        BusKeys.STATUS: "success",
        BusKeys.ACTION: LayerActions.NONE
    }
    return response


# ROUTES
@router.post("/down", response_model=VerifyResponse)
async def down(payload: PostBusMessage) -> dict[str, str]:
    # VERIFY PAYLOAD HERE
    return _bus_publish(BusDirections.DOWN, payload.model_dump())

@router.post("/up", response_model=VerifyResponse)
async def up(payload: PostBusMessage) -> dict[str, str]:
    # VERIFY PAYLOAD HERE
    return _bus_publish(BusDirections.UP, payload.model_dump())
    