# DEPENDENCIES
## Local
from .startup import ComponentTypes as Queues
from .startup import COMPONENT_TYPES


class QueueCommands:
    START: str = "nats-server -js"


# PUB/SUB
QUEUES: frozenset[str] = frozenset(
    [
        Queues.SENSES,
        Queues.MEMORY,
        Queues.ASPIRATIONAL,
        Queues.GLOBAL_STRATEGY,
        Queues.AGENT_MODEL,
        Queues.EXECUTIVE_FUNCTION,
        Queues.COGNITIVE_CONTROL,
        Queues.TASK_PROSECUTION,
    ]
)

## Busses
class BusDirections:
    UP: str = "up"
    DOWN: str = "down"

class BusKeys:
    STATUS: str = "status"
    ACTION: str = "action"

class BusSources:
    CONTROLLER: str = Queues.CONTROLLER
    LAYER: str = "layer"

BUSSES_DOWN: dict[str, str] = {
    Queues.CONTROLLER: Queues.ASPIRATIONAL,
    Queues.ASPIRATIONAL: Queues.GLOBAL_STRATEGY,
    Queues.GLOBAL_STRATEGY: Queues.AGENT_MODEL,
    Queues.AGENT_MODEL: Queues.EXECUTIVE_FUNCTION,
    Queues.EXECUTIVE_FUNCTION: Queues.COGNITIVE_CONTROL,
    Queues.COGNITIVE_CONTROL: Queues.TASK_PROSECUTION,
}

BUSSES_UP: dict[str, str] = {
    Queues.TASK_PROSECUTION: Queues.COGNITIVE_CONTROL,
    Queues.COGNITIVE_CONTROL: Queues.EXECUTIVE_FUNCTION,
    Queues.EXECUTIVE_FUNCTION: Queues.AGENT_MODEL,
    Queues.AGENT_MODEL: Queues.GLOBAL_STRATEGY,
    Queues.GLOBAL_STRATEGY: Queues.ASPIRATIONAL,
}