# DEPENDENCIES
## Third-Party
from fastapi import APIRouter
## Local
from constants.api import APIRoutes
from constants.queue import BusKeys
from constants.layer import LayerKeys, LayerCommands 
from components.layer.layer_messages import LayerSubMessage
from .models import BusMessage
from .service import bus_down, bus_up


# CONSTANTS
VONE_CHAT_ROUTE: str = f"{APIRoutes.VONE}/bus"


# API
router = APIRouter(
    prefix=VONE_CHAT_ROUTE,
    tags=["bus"],
    responses={404: {"description": "Not found"}}
)


# ROUTES
@router.post(f"/{BusKeys.DOWN}", response_model=tuple[LayerSubMessage, ...])
async def down(bus_message: BusMessage) -> tuple[LayerSubMessage, ...]:
    # VERIFY PAYLOAD HERE
    print(f"Bus Message: {bus_message.model_dump_json()}")
    bus_down(bus_message)
    response_dict: dict[str, str] = {LayerKeys.HEADING: LayerKeys.ACTIONS, LayerKeys.CONTENT: LayerCommands.NONE}
    response: tuple[LayerSubMessage, ...] = (LayerSubMessage.model_validate(response_dict),)
    return response

@router.post(f"/{BusKeys.UP}", response_model=tuple[LayerSubMessage, ...])
async def up(bus_message: BusMessage) -> tuple[LayerSubMessage, ...]:
    # VERIFY PAYLOAD HERE
    bus_up(bus_message)
    response_dict: dict[str, str] = {LayerKeys.HEADING: LayerKeys.ACTIONS, LayerKeys.CONTENT: LayerCommands.NONE}
    response: tuple[LayerSubMessage, ...] = (LayerSubMessage.model_validate(response_dict),)
    return response
    