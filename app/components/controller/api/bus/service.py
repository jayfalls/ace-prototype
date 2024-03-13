# DEPENDENCIES
## Built-in
import asyncio
import json
from threading import Thread
## Third-Party
from nats.aio.client import Client as NatsClient
from nats.js.client import JetStreamContext
from pydantic import ValidationError
## Local
from components import broker
from constants.layer import LayerKeys, LayerActions
from constants.queue import BusDirections, BUSSES_DOWN, BUSSES_UP
from .models import BusPublishPayload


# HELPERS
def _inverse(direction: str) -> str:
    return BusDirections.UP if direction == BusDirections.DOWN else BusDirections.DOWN


# QUEUE
async def _connect_and_publish(queue: str, message: str) -> None:
    nats_client: NatsClient
    nats_stream: JetStreamContext
    nats_client, nats_stream = await broker.connect()
    await broker.publish(stream=nats_stream, queue=queue, message=message)
    await nats_client.close()

def bus_publish(bus_direction: str, payload: dict[str, str]) -> None:
    try:
        queue_mapping: dict[str, str] = BUSSES_DOWN if bus_direction == BusDirections.DOWN else BUSSES_UP
        queue: str = queue_mapping.get(payload[LayerKeys.QUEUE], "")
        if not queue:
            print(f"Queue {payload[LayerKeys.QUEUE]} cannot send {bus_direction}!")
            return
        payload.pop(LayerKeys.QUEUE, None)

        payload[LayerKeys.SOURCE_DIRECTION] = _inverse(bus_direction)
        if LayerKeys.ACTION not in payload:
            payload[LayerKeys.ACTION] = LayerActions.NONE
        print(f"Sending {payload} to {queue}...")

        BusPublishPayload(**payload)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        thread = Thread(target=loop.run_until_complete, args=(_connect_and_publish(queue, json.dumps(payload)),))
        thread.start()
        thread.join()
    except ValidationError as error:
        raise error

def bus_down(payload: dict[str, str]) -> None:
    bus_publish(BusDirections.DOWN, payload)

def bus_up(payload: dict[str, str]) -> None:
    bus_publish(BusDirections.UP, payload)
