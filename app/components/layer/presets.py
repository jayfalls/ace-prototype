# DEPENDENCIES
## Built-In
from abc import ABC
## Local
from constants.layer import Layers, Telemetry, Access


# PRESETS
class LayerPreset(ABC):
    TELEMETRY: frozenset[str] = frozenset()

class Aspirational(LayerPreset):
    """
    The Aspirational class represents the ethical compass for an autonomous agent, aligning its values 
    and judgments to principles defined in its constitution.
    It processes inputs from all lower layers, issues moral judgments, sets mission 
    objectives, and makes ethical decisions.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {
            Telemetry.NONE
        }
    )

class GlobalStrategy(LayerPreset):
    """
    The GlobalStrategy class  is responsible for integrating real-world environmental context into the 
    agent's strategic planning and decision-making processes. It maintains an ongoing internal model of 
    the state of the broader environment outside of the agent itself by gathering sensory information 
    from external sources.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {
            Telemetry.TIME,
            Telemetry.LOCATION,
            Telemetry.WORLD_OVERVIEW,
            Telemetry.VISUAL,
            Telemetry.AUDIO,
            Telemetry.STDOUT,
            Telemetry.USER_INPUT
        }
    )

class AgentModel(LayerPreset):
    """
    The AgentModel class  is responsible for maintaining an extensive internal self-model of the agent's 
    capabilities, limitations, configuration, and state. This functional understanding of itself allows 
    the agent to ground its cognition in its actual capacities and shape strategic plans accordingly.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {
            Telemetry.MEMORY,
            Telemetry.EMBODIMENT,
            Telemetry.HARDWARE_STATS,
            Telemetry.SYSTEM_METRICS,
            Telemetry.SOFTWARE_STATS,
            Telemetry.SYSTEM_PROCESSES
        }
    )

class ExecutiveFunction(LayerPreset):
    """
    The Executive Function Layer is responsible for translating high-level strategic direction into 
    detailed and achievable execution plans. It focuses extensively on managing resources and risks.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {
            Telemetry.NONE
        }
    )

class CognitiveControl(LayerPreset):
    """
The Cognitive Control Layer is responsible for dynamic task switching and selection based on 
    environmental conditions and progress toward goals. It chooses appropriate tasks to execute 
    based on project plans from the Executive Function Layer.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {   
            Telemetry.SYSTEM_METRICS,
            Telemetry.SYSTEM_PROCESSES,
            Telemetry.LOCATION,
            Telemetry.VISUAL,
            Telemetry.AUDIO,
            Telemetry.STDOUT,
            Telemetry.USER_INPUT
        }
    )

class TaskProsecution(LayerPreset):
    """
    The Task Prosecution Layer is responsible for executing individual tasks and detecting success 
    or failure based on both environmental feedback and internal monitoring.
    """
    TELEMETRY: frozenset[str] = frozenset(
        {
            Telemetry.EMBODIMENT,
            Telemetry.LOCATION,
            Telemetry.SYSTEM_METRICS,
            Telemetry.SYSTEM_PROCESSES,
            Telemetry.VISUAL,
            Telemetry.AUDIO,
            Telemetry.STDOUT,
            Telemetry.USER_INPUT
        }
    )

LAYER_PRESET_MAP: dict[str, type[LayerPreset]] = {
    Layers.ASPIRATIONAL: Aspirational,
    Layers.GLOBAL_STRATEGY: GlobalStrategy,
    Layers.AGENT_MODEL: AgentModel,
    Layers.EXECUTIVE_FUNCTION: ExecutiveFunction,
    Layers.COGNITIVE_CONTROL: CognitiveControl,
    Layers.TASK_PROSECUTION: TaskProsecution
}
