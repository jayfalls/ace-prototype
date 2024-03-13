# DEPENDENCIES
## Built-in
import asyncio
from asyncio import Task
## Third-Party
from nats.aio.client import Client as NatsClient
## Local
from components import broker
from constants.settings import DebugLevels
from helpers import debug_print
from .bus import bus, get_message_from_bus


# BUS
async def layer_broker(queue: str) -> None:
    bus.queue = queue
    await asyncio.sleep(10)
    nats_client = NatsClient()
    try:
        nats_client, stream = await broker.connect()
        task: Task = asyncio.ensure_future(broker.subscribe(stream=stream, handler=get_message_from_bus, queue=queue, consumer=queue))
        await task
    except Exception as error:
        debug_print(f"ConnectionClosedError: {error}...", DebugLevels.ERROR)
    await nats_client.close()


# MAIN
def component(component_type: str) -> None:
    asyncio.run(layer_broker(queue=component_type))
