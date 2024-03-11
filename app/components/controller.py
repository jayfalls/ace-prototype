# DEPENDENCIES
## Built-in
import os
from typing import Union
## Third-Party
import toml
import uvicorn
## Local
from .api import run
from constants.api import RUNTIME_CONFIG_PATH, SETTINGS_PATH
from constants.startup import DevVolumePaths


# SETUP
def setup(local_mode: bool) -> None:
    print("\nSetting Up Controller Files...")
    settings_path: str = SETTINGS_PATH
    if local_mode:
        dirs: tuple[str, ...] = (DevVolumePaths.CONTROLLER_STORAGE_PATH, DevVolumePaths.OUTPUT_STORAGE_PATH)
        _ = [os.makedirs(dirs, exist_ok=True) for dirs in dirs]
        settings_path = DevVolumePaths.CONTROLLER_SETTINGS_PATH
    if not os.path.exists(settings_path):
        open(settings_path, 'a').close()
    
    with open(RUNTIME_CONFIG_PATH, 'w', encoding='utf-8') as config_file:
        runtime_config: dict[str, Union[bool, str]] = {
            "local_mode": local_mode,
            "settings_path": settings_path
        }
        toml.dump({'runtime': runtime_config}, config_file)


# MAIN
def main(local_mode: bool = False) -> None:
    setup(local_mode)
    print("\nStarting Server Client...")
    uvicorn.run(run.app, host="0.0.0.0", port=2349)
