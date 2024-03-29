# DEPENDENCIES
## Built-In
from typing import Callable
## Local
from constants.components import ComponentTypes


# SHARED
from .queue import broker


# STARTUP
from .controller import component as _controller
from .queue.component import component as _queue
from .telemetry import component as _telemetry
from .actions import component as _actions
from .memory import component as _memory
from .model_provider import component as _model_provider
from .layer import component as _layer

COMPONENT_MAP: dict[str, Callable[[str], None]] = {
    ComponentTypes.CONTROLLER: _controller,
    ComponentTypes.QUEUE: _queue,
    ComponentTypes.TELEMETRY: _telemetry,
    ComponentTypes.ACTIONS: _actions,
    ComponentTypes.MEMORY: _memory,
    ComponentTypes.MODEL_PROVIDER: _model_provider,
    ComponentTypes.ASPIRATIONAL: _layer,
    ComponentTypes.GLOBAL_STRATEGY: _layer,
    ComponentTypes.AGENT_MODEL: _layer,
    ComponentTypes.EXECUTIVE_FUNCTION: _layer,
    ComponentTypes.COGNITIVE_CONTROL: _layer,
    ComponentTypes.TASK_PROSECUTION: _layer,
}
