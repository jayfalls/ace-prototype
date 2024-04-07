# DEPENDENCIES
## Local
from constants.generic import GenericKeys
from helpers import debug_print
from constants.settings import DebugLevels
from ..layer_messages import LayerSubMessage


# STRING MANIPULATION
def build_text_from_sub_layer_messages(sub_messages: tuple[LayerSubMessage, ...], heading_identifier: str = "###") -> str:
    """
    Builds a text block from a LayerSubMessages.

    Arguments:
        sub_message (LayerSubMessage): The LayerSubMessage to build the text block from.
        heading_identifier (str): The string to use as the heading identifier (Default is ###).

    Returns:
        str: The concatenated text block generated from the messages.
    """
    debug_print(f"Building text from {sub_messages}...", DebugLevels.INFO)
    text: str = ""
    for sub_message in sub_messages:
        text += f"{heading_identifier} {sub_message.heading.title()}\n"
        if not sub_message.content:
            text += f"- {GenericKeys.NONE}"
            return text
        items: list[str] = [f"- {item}" for item in sub_message.content]
        text += "\n".join(items)
        text += "\n\n"
    return text


# EXTERNAL SOURCES
def get_telemetry(telemetry: frozenset[str]) -> str:
    # TODO: get telemetry then _build_text_from_dict
    return "- None"
