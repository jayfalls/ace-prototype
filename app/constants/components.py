"""
Component constants for the ace_prototype.
"""

class ComponentTypes:
    """Enum"""
    CONTROLLER: str = "controller"
    QUEUE: str = "queue"
    TELEMETRY: str = "telemetry"
    ACTIONS: str = "actions"
    MEMORY: str = "memory"
    MODEL_PROVIDER: str = "model_provider"
    ASPIRATIONAL: str = "aspirational"
    GLOBAL_STRATEGY: str = "global_strategy"
    AGENT_MODEL: str = "agent_model"
    EXECUTIVE_FUNCTION: str = "executive_function"
    COGNITIVE_CONTROL: str = "cognitive_control"
    TASK_PROSECUTION: str = "task_prosecution"

COMPONENT_TYPES: tuple = (
    ComponentTypes.CONTROLLER,
    ComponentTypes.QUEUE,
    ComponentTypes.TELEMETRY,
    ComponentTypes.ACTIONS,
    ComponentTypes.MEMORY,
    ComponentTypes.MODEL_PROVIDER,
    ComponentTypes.ASPIRATIONAL,
    ComponentTypes.GLOBAL_STRATEGY,
    ComponentTypes.AGENT_MODEL,
    ComponentTypes.EXECUTIVE_FUNCTION,
    ComponentTypes.COGNITIVE_CONTROL,
    ComponentTypes.TASK_PROSECUTION
)