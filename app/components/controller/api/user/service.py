# DEPENDENCIES
## Third-Party
import toml
## Local
from constants.api import RUNTIME_CONFIG_PATH


def test_toml() -> None:
    runtime_config: dict = {}
    with open(RUNTIME_CONFIG_PATH, 'r', encoding='utf-8') as config_file:
        config_str: str = config_file.read()
        runtime_config = toml.loads(config_str).get('runtime', {})
    settings: dict = {}
    with open(runtime_config.get('settings_path', ''), 'r', encoding='utf-8') as settings_file:
        settings_str: str = settings_file.read()
        settings = toml.loads(settings_str)
