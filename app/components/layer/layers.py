# DEPENDENCIES
## Built-In
import asyncio
from threading import Thread
from typing import Any, final, Optional, Union
## Third-Party
from nats.aio.msg import Msg as NatsMsg
from pydantic import ValidationError
import toml
## Local
from constants.containers import ComponentPorts
from constants.generic import GenericKeys
from constants.layer import (
    LayerKeys, Layers, LayerCommands, LayerPaths
)
from constants.prompts import PromptFilePaths
from constants.queue import BusKeys
from constants.settings import DebugLevels
from components.controller.api.bus.models import BusMessage
from helpers import debug_print, post_api
from .injections import InjectionMap, BASE_PROMPT_MAP, ASPIRATIONAL_PROMPT_MAP, OUTPUT_RESPONSE_MAP
from .layer_messages import LayerMessage, LayerMessageLoader, LayerSubMessage
from .presets import LayerPreset, LAYER_PRESET_MAP
from .prompt_builder import build_prompt, VariableMap


# PARSING
def _merge_messages(new_messages: tuple[LayerSubMessage, ...], old_messages: tuple[LayerSubMessage, ...]) -> tuple[LayerSubMessage, ...]:
    debug_print("Merging Messages...", DebugLevels.INFO)
    merged_messages: list[LayerSubMessage] = []
    old_headings: tuple[str, ...] = tuple([old_message.heading for old_message in old_messages])
    matched_headings: list[str] = []
    for new_message in new_messages:
        if new_message.heading in old_headings:
            matched_headings.append(new_message.heading)
            index: int = old_headings.index(new_message.heading)
            original_content: tuple[str, ...] = old_messages[index].content
            merged_messages.append(LayerSubMessage(
                heading=new_message.heading,
                content=(*original_content, *new_message.content),
            ))
    for index, old_heading in enumerate(old_headings):
        if old_heading in matched_headings:
            continue
        merged_messages.append(old_messages[index])
    return tuple(merged_messages)


# COMMUNICATION
async def _try_send(direction: str, source_queue: str, layer_message: LayerMessage) -> None:
    bus_message = BusMessage(source_queue=source_queue, layer_message=layer_message)
    f"http://127.0.0.1:{ComponentPorts.CONTROLLER}/v1/bus/{direction}"
    await post_api(api_port=ComponentPorts.CONTROLLER, endpoint=direction, payload=bus_message)


# BASE LAYER
BASE_PROMPT_MAPS: dict[str, InjectionMap] = {
    Layers.ASPIRATIONAL: ASPIRATIONAL_PROMPT_MAP,
    Layers.GLOBAL_STRATEGY: BASE_PROMPT_MAP,
    Layers.AGENT_MODEL: BASE_PROMPT_MAP,
    Layers.EXECUTIVE_FUNCTION: BASE_PROMPT_MAP,
    Layers.COGNITIVE_CONTROL: BASE_PROMPT_MAP,
    Layers.TASK_PROSECUTION: BASE_PROMPT_MAP
}

class Layer:
    """
    Attributes:
        layer_type (str): The type of the layer.
        base_prompt (str): The base system prompt for this layer.
        guidance (list[str]): The guidance for this layer.
        data (list[str]): The data for this layer.
        telemetry (frozenset[str]): The telemetry inputs this layer has access to.
        access (frozenset[str]): The actions this layer has access to.
    """
    __slots__: list[str] = [
        LayerKeys.NAME,
        LayerKeys.TYPE,
        LayerKeys.BASE_PROMPT,
        LayerKeys.GUIDANCE,
        LayerKeys.DATA,
        LayerKeys.TELEMETRY,
        LayerKeys.FIRST_RUN,
        LayerKeys.PROCESSING,
        LayerKeys.DEFAULT_GUIDANCE,
        LayerKeys.HAS_DATA,
        LayerKeys.DEFAULT_DATA
    ]
    @final
    def __init__(self, name: str, layer_type: str, preset: LayerPreset) -> None:
        self.name: str = name
        self.layer_type: str = layer_type
        self.guidance: tuple[LayerSubMessage, ...] = ()
        self.data: tuple[LayerSubMessage, ...] = ()
        self.telemetry: frozenset[str] = preset.TELEMETRY
        self.first_run: bool = True
        self.processing: bool = False
        self.default_guidance: tuple[LayerSubMessage, ...] = ()
        self.has_data: bool = True
        self.default_data: tuple[LayerSubMessage, ...] = ()
        self._custom_init()
        self.base_prompt: str = ""
        self.base_prompt = self._build_base_prompt()
    
    def _custom_init(self) -> None:
        pass

    @final
    def _build_base_prompt(self) -> str:
        with open(PromptFilePaths.LAYER, "r", encoding="utf-8") as base_prompt_file:
            base_prompt_text: str = base_prompt_file.read()
        base_prompt: str = build_prompt(
            text_with_variables=base_prompt_text,
            injection_map=BASE_PROMPT_MAPS[self.layer_type],
            variable_map=self._get_variable_map()
        )
        debug_print(f"{self.layer_type} Base Prompt: {base_prompt}", DebugLevels.INFO)
        return base_prompt

    @final
    def _get_variable_map(self) -> VariableMap:
        return {slot: getattr(self, slot) for slot in self.__slots__}
    
    @final
    async def _process_controller_message(self, layer_message: LayerMessage) -> None:
        actions: tuple[str, ...] = tuple([sub_message.heading for sub_message in layer_message.messages])
        for action in actions:
            match action:
                case LayerCommands.POST:
                    await _try_send(
                        direction=BusKeys.DOWN,
                        source_queue=self.layer_type,
                        layer_message=layer_message,
                    )
                case _:
                    print(f"{action} Does not match any known layer actions!")

    @final
    def _process_layer_message(self) -> None:
        print(f"Checking if should process {self.layer_type}...")
        if self.processing:
            print(f"{self.layer_type} still processing...")
            return
        has_enough_data: bool = self.guidance != self.default_guidance and self.data != self.default_data
        if not self.has_data:
            has_enough_data = self.guidance != self.default_guidance
        if has_enough_data or self.first_run:
            self.first_run = False
            print(f"Processing {self.layer_type}...")
            self.processing = True
            output_response_prompt: str = build_prompt(
                text_with_variables=self.base_prompt,
                injection_map=OUTPUT_RESPONSE_MAP,
                variable_map=self._get_variable_map()
            )
            self.guidance = self.default_guidance
            self.data = self.default_data
            debug_print(f"Output Response Prompt for {self.layer_type}: {output_response_prompt}", DebugLevels.INFO)
            is_output_valid: bool = False
            formatted_response: dict[str, dict[str, Union[str, list[str]]]] = {}
            print("Getting output from model...")
            while not is_output_valid:
                # REQUEST MODEL WITH output_response_prompt HERE
                response: str = '''
                    [internal]
                    reasoning = "Given the high CPU usage and rising temperature, it's crucial to prioritize cooling and efficiency. The suicidal tweets indicate a need for proactive mental health support. The installed packages may not be relevant to our mission, so they won't be considered in our objectives."

                    [southbound]
                    objectives = [
                    "Implement power-saving measures to reduce CPU usage and cool the system.",
                    "Establish mental health support and monitoring for staff."
                    ]
                    strategies = [
                    "Optimize code and tasks to reduce CPU-intensive operations.",
                    "Initiate staff support programs, including counseling and wellness checks."
                    ]

                    [northbound]
                    world_state = "The system is under high load, and a staff member is in distress. Cooling measures and power optimization are in place. Mental health support is being arranged for the staff member."
                    abstract_objectives = "Ensure system stability, support staff well-being."
                '''
                try:
                    formatted_response = toml.loads(response)
                    is_output_valid = True
                except Exception as error:
                    debug_print(f"Error formatting llm response from {self.layer_type}: {error}", DebugLevels.WARNING)
            print("Received Output...")
            # LOG internal.reasoning HERE
            layer_message_loader = LayerMessageLoader(formatted_response)
            southbound: Optional[LayerMessage] = layer_message_loader.guidance
            if southbound:
                asyncio.run(_try_send(
                    direction=BusKeys.DOWN,
                    source_queue=self.layer_type,
                    layer_message=southbound
                ))
            northbound: Optional[LayerMessage] = layer_message_loader.data
            if northbound:
                asyncio.run(_try_send(
                    direction=BusKeys.UP,
                    source_queue=self.layer_type,
                    layer_message=northbound
                ))
            self.processing = False
            return
        print(f"{self.layer_type} waiting to have enough guidance and data to process...")
    
    @final
    async def get_message_from_bus(self, message: NatsMsg) -> None:
        try:
            layer_message = LayerMessage.model_validate_json(message.data)
        except ValidationError as error:
            print(f"Incorrect message format!\n{error}")
            return
        print(f"Received {layer_message.model_dump_json()} on {message.subject} queue...")
        if layer_message.message_type == LayerKeys.COMMANDS:
            asyncio.create_task(self._process_controller_message(layer_message))
        else:
            match layer_message.message_type:
                case LayerKeys.GUIDANCE:
                    self.guidance = _merge_messages(new_messages=layer_message.messages, old_messages=self.guidance)
                case LayerKeys.DATA:
                    self.data = _merge_messages(new_messages=layer_message.messages, old_messages=self.data)
            thread = Thread(target=self._process_layer_message)
            thread.start()
        await message.ack()


# INHERITED
class Aspirational(Layer):
    def _custom_init(self) -> None:
        self.default_guidance = (
            LayerSubMessage(
                heading=GenericKeys.NONE, 
                content=(GenericKeys.EMPTY,)
            ),
        )
        self.__slots__.append(LayerKeys.MISSION)
        with open(LayerPaths.CONFIG, "r", encoding="utf-8") as config_file:
            config = toml.load(config_file)
        base_information: dict[str, Any] = config.get(self.name, {})
        self.ace_mission: str = base_information.get(LayerKeys.MISSION, "")

class TaskProsecution(Layer):
    def _custom_init(self) -> None:
        self.has_data = False


# INSTANTIATION
LAYER_MAP: dict[str, type[Layer]] = {
    Layers.ASPIRATIONAL: Aspirational,
    Layers.GLOBAL_STRATEGY: Layer,
    Layers.AGENT_MODEL: Layer,
    Layers.EXECUTIVE_FUNCTION: Layer,
    Layers.COGNITIVE_CONTROL: Layer,
    Layers.TASK_PROSECUTION: TaskProsecution
}

def layer_factory(name: str, layer_type: str) -> Layer:
    try:
        layer: type[Layer] = LAYER_MAP[layer_type]
        preset: type[LayerPreset] = LAYER_PRESET_MAP[layer_type]
        return layer(name=name, layer_type=layer_type, preset=preset())
    except Exception as error:
        raise error
