# DEPENDENCIES
## Built-in
import subprocess
## Local
from config import Settings
from constants.settings import DebugLevels
from exceptions.error_handling import exit_on_error


# HELPERS
def debug_print(message: str, debug_level: int) -> None:
    if Settings.DEBUG_LEVEL >= debug_level:
        print(message)

def execute(command: str, ignore_error: bool = False, error_message: str = "", debug_level: int = 0) -> str:
    if not error_message:
        error_message = f"Unable to execute command: {command}"
    debug_print(f"Running Command: {command}", debug_level=4)
    command_list: tuple[str, ...] = tuple(command.split())
    result = subprocess.run(command_list, capture_output=True, text=True)
    debug_print(result.stdout, debug_level=debug_level)
    if result.returncode != 0 and not ignore_error:
        exit_on_error(f"{error_message}\n{result.stderr}")
    return result.stdout

def exec_check_exists(check_command: str, keyword: str) -> bool:
    debug_print(f"\nChecking using {check_command} for {keyword}...", DebugLevels.DEBUG)
    existing: frozenset = frozenset(execute(check_command, debug_level=DebugLevels.DEBUG).split("\n"))
    debug_print(f"Existing Terms: {existing}", DebugLevels.DEBUG)
    for entry in existing:
        if keyword in entry:
            return True
    return False