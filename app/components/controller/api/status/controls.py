# DEPENDENCIES
## Third-Party
from pydantic import ValidationError
## Local
from constants.layer import LayerKeys, LayerActions
from constants.queue import Queues
from ..bus.service import bus_down
from ..bus.models import PostBusMessage


# PRIVATE
def _power_on_self_test() -> None:
    post_payload: dict[str, str] = {
        LayerKeys.QUEUE: Queues.CONTROLLER,
        LayerKeys.MESSAGE: LayerActions.NONE,
        LayerKeys.ACTION: LayerActions.POST,
    }
    try:
        PostBusMessage(**post_payload)
        bus_down(post_payload)
    except ValidationError as error:
        raise error
    except Exception as error:
        raise error
    


# PUBLIC
def start_ace() -> None:
    try:
        _power_on_self_test()
    except Exception as error:
        raise error