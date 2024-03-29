"""
Model Provider constants for the ace_prototype.
"""

class LLMKeys:
    """Enum"""
    API_KEY: str = "api_key"
    MODEL: str = "model"
    CONTEXT: str = "context"
    TEMPERATURE: str = "temperature"

class Providers:
    """Enum"""
    CLAUDE: str = "claude"
    GROQ: str = "groq"
    OLLAMA: str = "ollama"
    OPENAI: str = "openai"

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

class OpenAIModels:
    """Enum"""
    FOUR: str = "gpt-4"
    FOUR_TURBO: str = "gpt-4-turbo-preview"
    THREE_POINT_FIVE: str = "gpt-3.5-turbo"
