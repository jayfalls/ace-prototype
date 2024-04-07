# DEPENDENCIES
## Built-in
import subprocess
from subprocess import Popen
import sys
from typing import IO, Optional
## Third-Party
import aiohttp
from pydantic import BaseModel
## Local
from config import Settings
from constants.api import APIRoutes
from constants.containers import ComponentPorts
from constants.settings import DebugLevels
from exceptions.error_handling import exit_on_error


# LOGGING
def debug_print(message: str, debug_level: int = DebugLevels.INFO, end: Optional[str] = None) -> None:
    if not Settings.DEBUG_LEVEL >= debug_level:
        return
    if end:
        print(message, end=end)
    else:    
        print(message)


# SHELL
def execute(
    command: str,
    should_print_result: bool = True,
    ignore_error: bool = False,
    error_message: str = "",
    debug_level: int = DebugLevels.ERROR
) -> str:
    if not error_message:
        error_message = f"Unable to execute command: {command}"
    debug_print(f"Running Command: {command}", debug_level=4)
    command_list: tuple[str, ...] = tuple(command.split())
    process: Popen = subprocess.Popen(command_list, stdout=subprocess.PIPE, text=True)
    if should_print_result:
        has_printed: bool = False
        while process.poll() is None:
            if not process.stdout:
                continue
            print_lines: IO = process.stdout
            if has_printed:
                for _ in print_lines:
                    sys.stdout.write("\033[F")  # Move cursor up one line
                    sys.stdout.write("\033[K") # Clear line
            for line in print_lines:
                debug_print(line, debug_level=debug_level, end="")
            has_printed = True
    if process.returncode != 0 and not ignore_error:
        exit_on_error(f"{error_message}\n{process.stderr}")
    stdout, stderr = process.communicate()
    return stdout

def exec_check_exists(check_command: str, keyword: str) -> bool:
    debug_print(f"\nChecking using {check_command} for {keyword}...", DebugLevels.DEBUG)
    existing: frozenset = frozenset(execute(check_command, debug_level=DebugLevels.DEBUG).split("\n"))
    debug_print(f"Existing Terms: {existing}", DebugLevels.DEBUG)
    for entry in existing:
        if keyword in entry:
            return True
    return False


# API REQUESTS
async def get_api(api_port: str, endpoint: str, payload: BaseModel) -> str:
    if api_port not in ComponentPorts.get_frozen_values():
        raise ValueError(f"Invalid API Port: {api_port}")
    print(f"Send Payload: {payload.model_dump_json()}")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=f"http://127.0.0.1:{api_port}{APIRoutes.VONE}/{endpoint}", 
            data=payload.model_dump_json(), 
            headers={'Content-Type': 'application/json'}
        ) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html: str = await response.text()
            print("Body:", html, "...")
            return html

async def post_api(api_port: str, endpoint: str, payload: BaseModel) -> str:
    if api_port not in ComponentPorts.get_frozen_values():
        raise ValueError(f"Invalid API Port: {api_port}")
    print(f"Send Payload: {payload.model_dump_json()}")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=f"http://127.0.0.1:{api_port}{APIRoutes.VONE}/{endpoint}", 
            data=payload.model_dump_json(), 
            headers={'Content-Type': 'application/json'}
        ) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            html: str = await response.text()
            print("Body:", html, "...")
            return html
