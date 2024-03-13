# DEPENDENCIES
## Built-in
import json
from typing import Optional
## Third-Party
import aiohttp
from nats.aio.msg import Msg as NatsMsg
## Local
from constants.layer import LayerKeys, LayerActions
from constants.queue import BusDirections


# STATE
class Bus:
    __slots__: tuple[str, ...] = (
        "queue",
    )

bus = Bus()


# COMMUNICATION
async def _try_send(direction: str, message: str, action: Optional[str] = "") -> None:
    send_payload: dict[str, str] = {
        LayerKeys.QUEUE: bus.queue,
        LayerKeys.MESSAGE: message,
        LayerKeys.ACTION: action
    }
    json_data: str = json.dumps(send_payload)
    print(f"Send Payload: {send_payload}")
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:2349/v1/bus/{direction}", data=json_data, headers={'Content-Type': 'application/json'}) as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html, "...")


# PROCESSOR
async def _process_controller_message(payload: dict[str, str]) -> None:
    action: str = payload.get(LayerKeys.ACTION, "")
    match action:
        case LayerActions.POST:
            await _try_send(direction=BusDirections.DOWN, message=payload.get(LayerKeys.MESSAGE, ""), action=payload.get(LayerKeys.ACTION, ""))
        case _:
            print(f"{action} Does not match any known layer actions!")

async def _process_layer_message(payload: dict[str, str]) -> None:
    print("Layer Ops")

async def _process_bus_message(payload: dict[str, str]) -> None:
    if payload.get(LayerKeys.ACTION, "") != LayerActions.NONE:
        await _process_controller_message(payload)
        return
    await _process_layer_message(payload)


# HANDLER
async def get_message_from_bus(message: NatsMsg) -> None:
    data: dict[str, str] = {}
    try:
        data = json.loads(message.data.decode())
    except Exception as error:
        print("Incorrect message format!")
        return
    print(f"Received {data} from {message.subject}...")
    await _process_bus_message(data)
    await message.ack()
