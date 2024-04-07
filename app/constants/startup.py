"""
Startup constants for the ace_prototype.
"""

# DEPENDENCIES
## Local
from helpers import BaseEnum


class StartupCommands(BaseEnum):
    """Enum"""
    UPDATE: str = "git pull"
