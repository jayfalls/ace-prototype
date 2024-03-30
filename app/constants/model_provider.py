"""
Model Provider constants for the ace_prototype.
"""

# DEPENDENCIES
## Local
from .containers import VolumePaths

class LLMKeys:
    """Enum"""
    MODEL_TYPE: str = "model_type"
    PROVIDER_TYPE: str = "provider_type"

    # Config
    BASE_INFORMATION: str = "base_information"
    CURRENT_MAPPING: str = "current_mapping"

    # Provider Details
    API_KEY: str = "api_key"
    MODEL: str = "model"
    CONTEXT: str = "context"
    TEMPERATURE: str = "temperature"
    RATE_LIMIT: str = "rate_limit"
    LOW_VRAM: str = "low_vram"

class ModelProviderPaths:
    """Enum"""
    CONFIG: str = f"{VolumePaths.HOST_LAYERS}/.config"

class LLMStackTypes:
    """Enum"""
    GENERALIST: str = "generalist"
    EFFICIENT: str = "efficient"
    CODER: str = "coder"
    FUNCTION_CALLER: str = "function_caller"
    EMBEDDER: str = "embedder"
    RERANKER: str = "reranker"

LLM_STACK_TYPES: frozenset[str] = frozenset(vars(LLMStackTypes).values())

class ModelTypes:
    """Enum"""
    LLM: str = "llm"
    EMBEDDER: str = "embedder"
    RERANKER: str = "reranker"


# PROVIDERS
class Providers:
    """Enum"""
    CLAUDE: str = "claude"
    GROQ: str = "groq"
    OLLAMA: str = "ollama"
    OPENAI: str = "openai"
    FAST_EMBED: str = "fast_embed"
    RAGATOUILLE: str = "ragatouille"
    CROSS_ENCODER: str = "cross_encoder"

class ClaudeModels:
    """Enum"""
    OPUS: str = "claude-3-opus-20240229"
    SONNET: str = "claude-3-sonnet-20240229"
    HAIKU: str = "claude-3-haiku-20240307"

class GroqModels:
    """Enum"""
    MIXTRAL: str = "mixtral-8x7b-32768"

class OllamaModels:
    """Enum"""
    ALPHAMONARCH: str = "alphamonarch"
    PHI_TWO_ORANGE: str = "phi2-orange"
    STABLELM_TWO_ZEPHYR: str = "stablelm2:1.6b-zephyr-q6_K"
    DEEPSEEK_CODER: str = "deepseek-coder:6.7b-instruct-q3_K_L"
    DEEPSEEK_CODER_SMALL: str = "deepseek-coder:1.3b-instruct-q6_K"
    GORILLA_OPENFUNCTIONS: str = "adrienbrault/gorilla-openfunctions-v2:Q3_K_L"

class OpenAIModels:
    """Enum"""
    FOUR: str = "gpt-4"
    FOUR_TURBO: str = "gpt-4-turbo-preview"
    THREE_POINT_FIVE: str = "gpt-3.5-turbo"

class RagatouilleModels:
    """Enum"""
    MXBAI_COLBERT: str = "mixedbread-ai/mxbai-colbert-large-v1"

class FastEmbedModels:
    """Enum"""
    MXBAI_EMBED: str = "mixedbread-ai/mxbai-embed-large-v1"

class CrossEncoderModels:
    """Enum"""
    MXBAI_RERANKER: str = "mixedbread-ai/mxbai-rerank-large-v1"
