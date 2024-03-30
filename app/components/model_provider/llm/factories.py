# DEPENDENCIES
## Local
from constants.model_provider import LLMKeys, LLMStackTypes, LLM_STACK_TYPES, Providers
from .llms import (
    LLM, LLMDetails, OllamaDetails,
    ClaudeLLM, GroqLLM, OllamaLLM, OpenAILLM
)
from .rag import (
    Embedder, Reranker, RAGDetails,
    FastEmbed, Ragatouille, CrossEncoder
)


# INDIVIDUAL
def _llm_factory(llm: str, llm_details: dict[str, str]) -> LLM:
    generic_details = LLMDetails(
        api_key=llm_details[LLMKeys.API_KEY],
        model=llm_details[LLMKeys.MODEL]
    )
    match llm:
        case Providers.CLAUDE:
            return ClaudeLLM(generic_details)
        case Providers.GROQ:
            return GroqLLM(generic_details)
        case Providers.OLLAMA:
            ollama_details = OllamaDetails(
                model=llm_details[LLMKeys.MODEL],
                low_vram=True
            )
            return OllamaLLM(ollama_details)
        case Providers.OPENAI:
            return OpenAILLM(generic_details)
        case _:
            raise NotImplementedError(f"{llm} is not implemented...")

def _embedder_factory(embedder: str, details: dict[str, str]) -> Embedder:
    embedder_details = RAGDetails(
        model=details[LLMKeys.MODEL]
    )
    match embedder:
        case Providers.FAST_EMBED:
            return FastEmbed(embedder_details)
        case _:
            raise NotImplementedError(f"{embedder} is not implemented...")

def _reranker_factory(reranker: str, details: dict[str, str]) -> Reranker:
    reranker_details = RAGDetails(
        model=details[LLMKeys.MODEL]
    )
    match reranker:
        case Providers.RAGATOUILLE:
            return Ragatouille(reranker_details)
        case Providers.CROSS_ENCODER:
            return CrossEncoder(reranker_details)
        case _:
            raise NotImplementedError(f"{reranker} is not implemented...")


# FULL MODEL PROVIDER
class LLMStack:
    """
    A class that provides a stack of LLMs for use in the ace pipeline

    Arguments:
        provider_map (dict[str, dict[str, str]]): A map of different provider stacks. The details should include the following keys:
            - model_type (str): The type of model that is being used. Either `llm` | `embedder` | `reranker`
            - provider_type (str): The type of provider that is being used. This should be one of the values in `constants.model_provider.Providers`
            - api_key (str): The API key that is used to access the model
            - model (str): The name of the model that is being used

    Attributes:
        generalist (LLM): A generalist LLM that can be used for any task
        efficient (LLM): A cheap & fast LLM used for more basic tasks 
        coder (LLM): An LLM that is specifically trained for coding tasks
        function_caller (LLM): An LLM that is specifically trained for function calling tasks
        embedder (Embedder): A model that can be used for embedding tasks
        reranker (Reranker): A model that can be used for reranking tasks
    """
    __slots__: tuple[str, ...] = (
        LLMStackTypes.GENERALIST,
        LLMStackTypes.EFFICIENT,
        LLMStackTypes.CODER,
        LLMStackTypes.FUNCTION_CALLER,
        LLMStackTypes.EMBEDDER,
        LLMStackTypes.RERANKER
    )
    def __init__(self, provider_map: dict[str, dict[str, str]]) -> None:        
        valid_details_identifiers: frozenset[str] = frozenset({
            LLMKeys.MODEL_TYPE,
            LLMKeys.PROVIDER_TYPE,
            LLMKeys.API_KEY,
            LLMKeys.MODEL
        })
        for _, provider_details in provider_map.items():
            provider_map_keys: frozenset[str] = frozenset(provider_details.keys())
            valid_details: bool = valid_details_identifiers.issuperset(provider_map_keys)
            if not valid_details:
                raise ValueError(f"Provider config is missing required details: {valid_details_identifiers - provider_map_keys}")

        llm_map: dict[str, LLM] = {}
        embedder_map: dict[str, Embedder] = {}
        reranker_map: dict[str, Reranker] = {}
        for stack_type in LLM_STACK_TYPES:
            provider_details: dict[str, str] = provider_map[stack_type]
            _, model_type = provider_details.popitem()
            _, provider_type = provider_details.popitem()
            match model_type:
                case LLMKeys.LLM:
                    llm_map[stack_type] = _llm_factory(provider_type, provider_details)
                case LLMKeys.EMBEDDER:
                    embedder_map[stack_type] = _embedder_factory(provider_type, provider_details)
                case LLMKeys.RERANKER:
                    reranker_map[stack_type] = _reranker_factory(provider_type, provider_details)
                case _:
                    raise NotImplementedError(f"{model_type} is not implemented...") 
            
        self.generalist: LLM = llm_map[LLMStackTypes.GENERALIST]
        self.efficient: LLM = llm_map[LLMStackTypes.EFFICIENT]
        self.coder: LLM = llm_map[LLMStackTypes.CODER]
        self.function_caller: LLM = llm_map[LLMStackTypes.FUNCTION_CALLER]
        self.embedder: Embedder = embedder_map[LLMStackTypes.EMBEDDER]
        self.reranker: Reranker = reranker_map[LLMStackTypes.RERANKER]
