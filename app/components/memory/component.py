# DEPENDENCIES
## Built-in
import asyncio
## Third-Party
from nats.aio.client import Client as NatsClient
from nats.aio.msg import Msg as NatsMsg
from nats.js.client import JetStreamContext
## Local
from components import broker
from constants.settings import DebugLevels
from helpers import debug_print


nats_client: NatsClient = NatsClient()
nats_stream: JetStreamContext = JetStreamContext(nats_client)


async def test_request(message: NatsMsg) -> None:
    print(f"Received a message on '{message.subject} {message.reply}': {message.data.decode()}")
    await broker.publish(stream=nats_stream, queue=message.reply, message="I can help")

async def nats_test(queue: str) -> None:
    nats_client = NatsClient()
    try:
        nats_client, nats_stream = await broker.connect()
        await broker.subscribe(stream=nats_stream, handler=test_request, queue=queue, consumer=queue)
    except Exception as error:
        debug_print(f"ConnectionClosedError: {error}...", DebugLevels.ERROR)
    await nats_client.close()

# MAIN
def component(component_type: str) -> None:
    asyncio.run(nats_test(queue=component_type))