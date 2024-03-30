# DEPENDENCIES
## Built-in
import os
from time import sleep
from typing import Any
## Third-Party
import toml
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
## Local
from constants.containers import VolumePaths
from constants.generic import GenericKeys, TOMLConfig
from constants.model_provider import (
    LLMKeys, LLMStackTypes, 
    ModelProviderPaths, 
    ModelTypes, Providers,
    OllamaModels, FastEmbedModels, RagatouilleModels
)
from constants.settings import DebugLevels
from helpers import debug_print
from .llm import LLMStack


llm_stack: LLMStack


# CONSTANTS
BASE_CONFIG: TOMLConfig = {
    LLMKeys.BASE_INFORMATION: {
        LLMKeys.CURRENT_MAPPING: GenericKeys.DEFAULT
    },
    GenericKeys.DEFAULT: {
        LLMStackTypes.GENERALIST: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.ALPHAMONARCH
        },
        LLMStackTypes.EFFICIENT: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.PHI_TWO_ORANGE
        },
        LLMStackTypes.CODER: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.DEEPSEEK_CODER
        },
        LLMStackTypes.FUNCTION_CALLER: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.GORILLA_OPENFUNCTIONS
        },
        LLMStackTypes.EMBEDDER: {
            LLMKeys.MODEL_TYPE: ModelTypes.EMBEDDER,
            LLMKeys.PROVIDER_TYPE: Providers.FAST_EMBED,
            LLMKeys.MODEL: FastEmbedModels.MXBAI_EMBED
        },
        LLMStackTypes.RERANKER: {
            LLMKeys.MODEL_TYPE: ModelTypes.RERANKER,
            LLMKeys.PROVIDER_TYPE: Providers.RAGATOUILLE,
            LLMKeys.MODEL: RagatouilleModels.MXBAI_COLBERT
        }
    },
    f"{GenericKeys.DEFAULT}_small": {
        LLMStackTypes.GENERALIST: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.PHI_TWO_ORANGE
        },
        LLMStackTypes.EFFICIENT: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.STABLELM_TWO_ZEPHYR
        },
        LLMStackTypes.CODER: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.DEEPSEEK_CODER_SMALL
        },
        LLMStackTypes.FUNCTION_CALLER: {
            LLMKeys.MODEL_TYPE: ModelTypes.LLM,
            LLMKeys.PROVIDER_TYPE: Providers.OLLAMA,
            LLMKeys.MODEL: OllamaModels.PHI_TWO_ORANGE
        },
        LLMStackTypes.EMBEDDER: {
            LLMKeys.MODEL_TYPE: ModelTypes.EMBEDDER,
            LLMKeys.PROVIDER_TYPE: Providers.FAST_EMBED,
            LLMKeys.MODEL: FastEmbedModels.MXBAI_EMBED
        },
        LLMStackTypes.RERANKER: {
            LLMKeys.MODEL_TYPE: ModelTypes.RERANKER,
            LLMKeys.PROVIDER_TYPE: Providers.RAGATOUILLE,
            LLMKeys.MODEL: RagatouilleModels.MXBAI_COLBERT
        }
    }
}


# SETUP
def _set_current_mapping(new_mapping: str) -> None:
    with open(ModelProviderPaths.CONFIG, "r", encoding="utf-8") as config_file:
        config: TOMLConfig = toml.load(config_file)
    config[LLMKeys.BASE_INFORMATION][LLMKeys.CURRENT_MAPPING] = new_mapping
    with open(ModelProviderPaths.CONFIG, "w", encoding="utf-8") as config_file:
        toml.dump(config, config_file)

def _setup() -> None:
    if os.path.isfile(ModelProviderPaths.CONFIG):
        with open(ModelProviderPaths.CONFIG, "r", encoding="utf-8") as config_file:
            existing_config: TOMLConfig = toml.load(config_file)
            base_information: dict[str, Any] = existing_config.get(LLMKeys.BASE_INFORMATION, {})
            current_mapping: str = base_information.get(LLMKeys.CURRENT_MAPPING, GenericKeys.NONE)
            if current_mapping in existing_config.keys():
                return
            _set_current_mapping(new_mapping=GenericKeys.DEFAULT)
        return
    global llm_stack
    llm_stack = LLMStack(provider_map=BASE_CONFIG[GenericKeys.DEFAULT])
    with open(ModelProviderPaths.CONFIG, "w", encoding="utf-8") as config_file:
        toml.dump(BASE_CONFIG, config_file)


# CONFIG LISTENER
class MonitorConfig(FileSystemEventHandler):
    def _get_config(self) -> TOMLConfig:
        with open(ModelProviderPaths.CONFIG, "r", encoding="utf-8") as config_file:
            config: TOMLConfig = toml.load(config_file)
        return config

    def _valid_config_change(self) -> bool:
        config: TOMLConfig = self._get_config()
        base_information: dict[str, Any] = config[LLMKeys.BASE_INFORMATION]
        current_mapping: str = base_information[LLMKeys.CURRENT_MAPPING]
        first_key = next(iter(config))  # Get the first key in the dictionary
        del config[first_key]
        if current_mapping not in config.keys():
            debug_print(f"Model provider mapping {current_mapping} does not exist! Create its config first before trying to instantiate it...", DebugLevels.ERROR)
            if self.current_mapping in config.keys():
                _set_current_mapping(new_mapping=self.current_mapping)
            else:
                _set_current_mapping(new_mapping=GenericKeys.NONE)
            return False
        if self.current_mapping == current_mapping:
            debug_print("ACE has not changed. Skipping...", DebugLevels.INFO)
            return False
        self.current_mapping = current_mapping
        return True

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return None
        try:
            if not self._valid_config_change():
                return

            global llm_stack
            config: TOMLConfig = self._get_config()
            current_mapping: str = config[LLMKeys.BASE_INFORMATION][LLMKeys.CURRENT_MAPPING]
            provider_map: dict[str, dict[str, str]] = config[current_mapping]
            llm_stack = LLMStack(provider_map)
        except Exception as error:
            raise error

def startup() -> None:
    _setup()
    event_handler = MonitorConfig()
    observer = Observer()
    observer.schedule(event_handler=event_handler, path=f"{VolumePaths.MODEL_PROVIDER}", recursive=False)
    observer.start()
    print("Listening for config changes...")
    try:
        while True:
           sleep(1)
    except Exception as error:
        debug_print(f"Layer Error: {error}...", DebugLevels.ERROR)
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.stop()
        observer.join()
