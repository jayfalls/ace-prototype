# DEPENDENCIES
## Built-In
from datetime import datetime
from functools import cache
from typing import Callable
## Third-Party
import httpx
## Local
from constants.telemetry import TelemetryTypes
from helpers import check_internet_access


# CONSTANTS
DEFAULT_CACHE_COUNT: int = 256
NEWS_API_KEY: str = "pub_42899f1e388aa15a48c2f2a4a74bf5b1af43b"

class TelemetryTypesRef():
    """Enum"""
    NONE: str = "none"
    TIME: str = "time"
    LOCATION: str = "location"
    EMBODIMENT: str = "embodiment"
    WORLD_OVERVIEW: str = "world_overview"
    HARDWARE_STATS: str = "hardware_statistics"
    SYSTEM_METRICS: str = "system_metrics"
    SOFTWARE_STATS: str = "software_statistics"
    SYSTEM_PROCESSES: str = "system_processes"
    RESOURCES: str = "resources"
    MEMORY: str = "memory"
    VISUAL: str = "visual"
    AUDIO: str = "audio"
    STDOUT: str = "stdout"
    USER_INPUT: str = "user_input"


# Collection Strategies
def _get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def _get_location() -> str:
    if check_internet_access():
        response: httpx.Response = httpx.get("https://ipapi.co/json/")
        data: dict[str, str] = response.json()
        city: str = data["city"]
        region: str = data["region"]
        country_name: str = data["country_name"]
        location: str = f"{city}, {region}, {country_name}"
        return f"{location}"
    else:
        return "Location unavailable"

def _get_embodiment() -> str:
    return "embodiment"

def _get_world_overview() -> str:
    return "world overview"

@cache
def _get_hardware_statistics() -> str:
    return "hardware statistics"

def _get_system_metrics() -> str:
    return "system metrics"

def _get_software_statistics() -> str:
    return "software statistics"

def _get_system_processes() -> str:
    return "system processes"

def _get_resources(context: str) -> str:
    return "resources"

def _get_memory(context: str) -> str:
    return "memory"

def _get_visual() -> str:
    return "visual"

def _get_audio() -> str:
    return "audio"

def _get_stdout() -> str:
    return "stdout"

def _get_user_input() -> str:
    return "user input"

ACCESS_CONTEXTLESS_STRATEGY_MAP: dict[str, Callable[[], str]] = {
    TelemetryTypes.NONE: lambda: TelemetryTypes.NONE,
    TelemetryTypes.TIME: _get_time,
    TelemetryTypes.LOCATION: _get_location,
    TelemetryTypes.EMBODIMENT: _get_embodiment,
    TelemetryTypes.WORLD_OVERVIEW: _get_world_overview,
    TelemetryTypes.HARDWARE_STATS: _get_hardware_statistics,
    TelemetryTypes.SYSTEM_METRICS: _get_system_metrics,
    TelemetryTypes.SOFTWARE_STATS: _get_software_statistics,
    TelemetryTypes.SYSTEM_PROCESSES: _get_system_processes,
    TelemetryTypes.VISUAL: _get_visual,
    TelemetryTypes.AUDIO: _get_audio,
    TelemetryTypes.STDOUT: _get_stdout,
    TelemetryTypes.USER_INPUT: _get_user_input
}

ACCESS_CONTEXTUAL_STRATEGY_MAP: dict[str, Callable[[str], str]] = {
    TelemetryTypes.RESOURCES: _get_resources,
    TelemetryTypes.MEMORY: _get_memory,
}

def collect_telemetry(access: frozenset[str], context: str) -> frozenset[str]:
    telemetry: list[str] = []
    for telemetry_type in access:
        if telemetry_type in ACCESS_CONTEXTLESS_STRATEGY_MAP:
            telemetry.append(ACCESS_CONTEXTLESS_STRATEGY_MAP[telemetry_type]())
        elif telemetry_type in ACCESS_CONTEXTUAL_STRATEGY_MAP:
            telemetry.append(ACCESS_CONTEXTUAL_STRATEGY_MAP[telemetry_type](context))
    return frozenset(telemetry)
