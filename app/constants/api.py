# DEPENDENCIES
## Built-in
import os
## Third-Party
from fastapi.templating import Jinja2Templates
## Local
from constants.startup import VolumePaths


module_path = os.path.realpath(__file__)

RUNTIME_CONFIG_PATH: str = f"{os.path.dirname(module_path)}/.config"
STORAGE_PATH: str = f"{VolumePaths.STORAGE_PATH}/controller"
SETTINGS_PATH: str = f"{STORAGE_PATH}/settings"
VONE_API_ROUTE: str = "/v1"
CONTROLLER_PATH: str = "components/controller"
API_PATH: str = f"{CONTROLLER_PATH}/api"
UI_PATH: str = f"{CONTROLLER_PATH}/ui"
HTML_TEMPLATES = Jinja2Templates(directory=f"{UI_PATH}/templates")
FAVICON_PATH: str = f"{UI_PATH}/assets/images/favicon.ico"