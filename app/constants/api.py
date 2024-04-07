"""
API constants for the ace_prototype.
"""


# DEPENDENCIES
## Third-Party
from fastapi.templating import Jinja2Templates
## Local
from helpers import BaseEnum
from .containers import VolumePaths
from .components import ComponentTypes
from .generic import Paths


class APIRoutes(BaseEnum):
    """Enum"""
    VONE: str = "/v1"

APIS: frozenset[str] = frozenset(
    {
        ComponentTypes.CONTROLLER,
        ComponentTypes.TELEMETRY,
        ComponentTypes.ACTIONS,
        ComponentTypes.MEMORY,
        ComponentTypes.MODEL_PROVIDER
    }
)

class APIPaths(BaseEnum):
    """Enum"""
    STORAGE: str = f"{VolumePaths.STORAGE}/controller"
    SETTINGS: str = f"{STORAGE}/settings"
    API: str = f"{Paths.CONTROLLER}/api"
    RUNTIME_CONFIG: str = f"{API}/.config"
    UI: str = f"{Paths.CONTROLLER}/ui"
    FAVICON: str = f"{UI}/assets/images/favicon.ico"

HTML_TEMPLATES = Jinja2Templates(directory=f"{APIPaths.UI}/templates")
