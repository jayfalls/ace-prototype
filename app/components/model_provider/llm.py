# DEPENDENCIES
## Built-In
from abc import ABC, abstractmethod
from typing import Any, Generic, Iterator, Mapping, TypeVar, Union
## Third-Party
from anthropic import Anthropic
from anthropic import Stream as AnthropicStream
from anthropic.types import MessageStreamEvent
from groq import Groq
from groq.types.chat import ChatCompletion as GroqChatCompletion
import ollama
from ollama import Options as OllamaOptions
from openai import OpenAI
from openai import Stream as OpenAIStream
from openai.types.chat import ChatCompletionChunk as OpenAIChatCompletionChunk
from pydantic import BaseModel
## Local
from constants.generic import GenericKeys
from constants.model_provider import (
    LLMKeys, 
    Providers, ClaudeModels, GroqModels, OllamaModels, OpenAIModels
)


# CONSTANTS
_ASSISTANT_BEGIN: str = '[internal]\nreasoning = """' # Must match the start of the response schemas


# PROVIDERS
class ProviderDetails(BaseModel):
    api_key: str
    model: str
    context: int = 4096
    temperature: float = 0.2

GenericProviderDetails = TypeVar("GenericProviderDetails", bound=ProviderDetails)

class Provider(ABC, Generic[GenericProviderDetails]):
    __slots__: tuple[str, ...] = (
        LLMKeys.API_KEY,
        LLMKeys.MODEL,
        LLMKeys.CONTEXT,
        LLMKeys.TEMPERATURE
    )
    def __init__(self, provider_details: GenericProviderDetails) -> None:
        self.api_key: str = provider_details.api_key
        self.model: str = provider_details.model
        self.context: int = provider_details.context
        self.temperature: float = provider_details.temperature
        self._custom_init(provider_details)
    
    def _custom_init(self, provider_details: GenericProviderDetails) -> None:
        pass

    @abstractmethod
    def generate(self, system_prompt: str) -> str:
        raise NotImplementedError

## Claude
class ClaudeProvider(Provider):
    def generate(self, system_prompt: str) -> str:
        client = Anthropic(api_key=self.api_key)
        stream: AnthropicStream[MessageStreamEvent] = client.messages.create(
            system=system_prompt,
            messages=[
                {
                    "role": "assistant",
                    "content": _ASSISTANT_BEGIN
                }
            ],
            model=self.model,
            max_tokens=self.context,
            temperature=self.temperature,
            stream=True,
        )
        output: list[str] = []
        for event in stream:
            output.append(event.type)
        return "".join(output)

## Groq
class GroqProvider(Provider):
    def generate(self, system_prompt: str) -> str:
        client = Groq(api_key=self.api_key)
        chat_completion: GroqChatCompletion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                }
            ],
            max_tokens=self.context,
            temperature=self.temperature,
            model=self.model,
        )
        return chat_completion.choices[0].message.content

## Ollama
class OllamaDetails(ProviderDetails):
    api_key: str = GenericKeys.NONE
    low_vram: bool = False

class OllamaProvider(Provider):
    def _custom_init(self, provider_details: OllamaDetails) -> None:
        self.__slots__ = (
            *self.__slots__,
            "low_vram"
        )
        self.low_vram: bool = provider_details.low_vram

    def generate(self, system_prompt: str) -> str:
        stream: Union[Mapping[str, Any], Iterator[Mapping[str, Any]]] = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "assistant",
                    "content": _ASSISTANT_BEGIN
                }
            ],
            options=OllamaOptions(
                num_ctx=self.context,
                temperature=self.temperature,
                low_vram=self.low_vram
            ),
            stream=True,
        )
        output: list[str] = []
        if isinstance(stream, Iterator):
            for chunk in stream:
                output.append(chunk["message"]["content"])
        else:
            output.append(stream["message"]["content"])
        return "".join(output)

## OpenAI
class OpenAIProvider(Provider):
    def generate(self, system_prompt: str) -> str:
        client = OpenAI(api_key=self.api_key)
        stream: OpenAIStream[OpenAIChatCompletionChunk] = client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "assistant",
                    "content": _ASSISTANT_BEGIN
                }
            ],
            max_tokens=self.context,
            temperature=self.temperature,
            stream=True,
        )
        output: list[str] = []
        for chunk in stream:
            output.append(chunk.choices[0].delta.content or "")
        return "".join(output)


# FACTORY
def get_llm_provider(provider: str, provider_details: ProviderDetails) -> Provider:
    match provider:
        case Providers.CLAUDE:
            if not isinstance(provider_details, ProviderDetails):
                raise TypeError(f"Provider Details must be of type ProviderDetails for {provider} provider")
            provider_details = ProviderDetails(
                api_key="TEST",
                model=ClaudeModels.HAIKU
            )
            return ClaudeProvider(provider_details)
        case Providers.GROQ:
            if not isinstance(provider_details, ProviderDetails):
                raise TypeError(f"Provider Details must be of type ProviderDetails for {provider} provider")
            provider_details = ProviderDetails(
                api_key="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",
                model=GroqModels.MIXTRAL
            )
            return GroqProvider(provider_details)
        case Providers.OLLAMA:
            if not isinstance(provider_details, OllamaDetails):
                raise TypeError(f"Provider Details must be of type OllamaDetails for {provider} provider")
            provider_details = OllamaDetails(
                model=OllamaModels.ALPHAMONARCH,
                low_vram=True
            )
            return OllamaProvider(provider_details)
        case Providers.OPENAI:
            if not isinstance(provider_details, ProviderDetails):
                raise TypeError(f"Provider Details must be of type ProviderDetails for {provider} provider")
            provider_details = ProviderDetails(
                api_key="TEST",
                model=OpenAIModels.THREE_POINT_FIVE
            )
            return OpenAIProvider(provider_details)
        case _:
            raise NotImplementedError(f"{provider} is not implemented...")
