#!/usr/bin/env python3
"""
Starting point for the ACE Prototype, as well as the individual components.

Author: jayfalls

Arguments:
    -d/--debug: bool -> Enable debug mode
    -t/--test: bool -> Run tests
    -b/--build: bool -> Build the images
    -nb/--no-build: bool -> Skip the build
    -s/--stop: bool -> Stop the ACE cluster
    -r/--restart: bool -> Restart the ACE cluster deployment
    -u/--update: bool -> Update the ACE
    -ct/--component-type: str -> The type of this component
"""


# DEPENDENCIES
## Built-in
from argparse import ArgumentParser
import os
import subprocess
import time
## Third Party
from exceptions.error_handling import exit_on_error
import pytest
## Local
from config import Settings, DebugSettings
from constants import (
    ComponentTypes, COMPONENT_TYPES, DebugLevels, Commands,
    StartupArgumentNames, STARTUP_BOOL_ARGUMENTS, STARTUP_STRING_ARGUMENTS, STARTUP_ARGUMENTS, STARTUP_ARGUMENTS_HELP,
    StartupArgumentsShort,
    ACE_IMAGE_NAME, ImageCommands,
    KUBE_POD_NAMES, KUBE_SERVICE_NAMES, ClusterCommands, VolumePaths
)
from components import (
    ui, controller, queue, model_provider, senses, memory, layer
)


# HELPERS
def debug_print(message: str, debug_level: int) -> None:
    if Settings.debug_level >= debug_level:
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


# VARIABLES
class ACEArguments:
    debug: bool = False
    should_test: bool = False
    should_build: bool = False
    no_build: bool = False
    stop: bool = False
    should_restart: bool = False
    should_update: bool = False
    component: str = ""


# SETUP
def setup() -> None:
    required_paths: tuple[str, ...] = ("./storage/output", "./storage/controller")
    _ = [os.makedirs(dir_path, exist_ok=True) for dir_path in required_paths]


# ARGUMENTS
def _set_arguments(arg_parser: ArgumentParser) -> None:
    for argument in STARTUP_BOOL_ARGUMENTS:
        arg_parser.add_argument(*tuple(STARTUP_ARGUMENTS.get(argument, "")), action='store_true', required=False, help=STARTUP_ARGUMENTS_HELP[argument])
    for argument in STARTUP_STRING_ARGUMENTS:
        arg_parser.add_argument(*tuple(STARTUP_ARGUMENTS.get(argument, "")), type=str, required=False, help=STARTUP_ARGUMENTS_HELP[argument])

def _parse_arguments(arg_parser: ArgumentParser) -> ACEArguments:
    arguments: dict = {key: value for key, value in vars(arg_parser.parse_args()).items() if value is not None}
    ace_arguments = ACEArguments()
    ace_arguments.debug = arguments.get(StartupArgumentNames.DEBUG, False)
    if ace_arguments.debug:
        global Settings
        Settings = DebugSettings
    ace_arguments.component = arguments.get(StartupArgumentNames.COMPONENT_TYPE, StartupArgumentNames.STARTUP)
    ace_arguments.should_test = arguments.get(StartupArgumentNames.TEST, False)
    ace_arguments.should_build = arguments.get(StartupArgumentNames.BUILD, False)
    ace_arguments.no_build = arguments.get(StartupArgumentNames.NO_BUILD, False)
    ace_arguments.stop = arguments.get(StartupArgumentNames.STOP, False)
    ace_arguments.should_update = arguments.get(StartupArgumentNames.UPDATE, False)
    ace_arguments.should_restart = arguments.get(StartupArgumentNames.RESTART, False)
    debug_print(f"Arguments: {ace_arguments.__dict__}", DebugLevels.DEBUG)
    if ace_arguments.component not in COMPONENT_TYPES and ace_arguments.component != StartupArgumentNames.STARTUP:
        exit_on_error(f"Invalid component type: {ace_arguments.component}!\nPlease use one of the following: {COMPONENT_TYPES}")
    return ace_arguments
    

def assign_arguments() -> ACEArguments:
    arg_parser = ArgumentParser()
    _set_arguments(arg_parser)
    ace_arguments: ACEArguments = _parse_arguments(arg_parser)
    return ace_arguments

    
## Building
def build(ace_arguments: ACEArguments) -> None:
    print("\nChecking if build is required...")
    print()
    check_images_command: str = ImageCommands.CHECK_IMAGES
    image_exists: bool = exec_check_exists(check_images_command, ACE_IMAGE_NAME)
    should_build: bool = not image_exists or ace_arguments.should_build
    if should_build:
        if not image_exists:
            print("Image does not exist\nBuilding container...")
        else:
            print("Building container...")
        build_ace_images_command: str = ImageCommands.BUILD_IMAGE
        execute(build_ace_images_command, error_message="Unable to build image")
        return
    print("Image already exists\nSkipping build...")

# TESTS
def _run_tests(tests_to_run: tuple[str, ...]) -> None:
    print("Running tests...")
    # Create a pytest argument parser
    args = ['--capture=no']

    # Add the names of the tests to run to the arguments list
    args.extend(tests_to_run)

    # Run the tests using pytest's main function
    pytest.main(args)

def test() -> None:
    print("\nTest Mode\n")
    class test_types:
        TEST1: str = "test1"
        TEST2: str = "test2"
    tests: tuple[str, ...] = (test_types.TEST1, test_types.TEST2)
    _run_tests(tests)


# RUNTIME
def update() -> None:
    print("\nUpdating ACE...")
    update_command: str = Commands.UPDATE_COMMAND
    execute(update_command)

def stop() -> None:
    unique_pod: str = KUBE_POD_NAMES[0]
    if not exec_check_exists(ClusterCommands.GET_PODS, unique_pod):
        exit_on_error("ACE is not running!")
    print("\nStopping ACE...")
    delete_pod_command: str = ClusterCommands.DELETE_POD
    for pod_name in KUBE_POD_NAMES:
        delete_command: str = f"{delete_pod_command} {pod_name}"
        execute(delete_command, ignore_error=True)
    delete_service_command: str = ClusterCommands.DELETE_SERVICE
    for service_name in KUBE_SERVICE_NAMES:
        delete_command: str = f"{delete_service_command} {service_name}"
        execute(delete_command, ignore_error=True)

def _create_cluster() -> bool:
    cluster_name: str = "ACE"
    if not exec_check_exists(ClusterCommands.GET_CLUSTER, cluster_name):
        print(f"\n{cluster_name} Cluster does not exist!\nCreating cluster...")
        create_cluster_command: str = ClusterCommands.CREATE_CLUSTER
        current_dir: str = os.path.abspath('.')
        volume_arguments: tuple[str, ...] = (
            f"-v {current_dir}/{VolumePaths.HOST_CONTROLLER}:{VolumePaths.CONTROLLER}",
            f"-v {current_dir}/{VolumePaths.HOST_OUTPUT}:{VolumePaths.OUTPUT}",
        )
        volumes_argument: str = " ".join(volume_arguments)
        create_command: str = f"{create_cluster_command} {volumes_argument}"
        full_create_command: tuple[str, ...] = (create_command, ClusterCommands.APPLY_CONFIG)
        _ = [execute(command) for command in full_create_command]
        return True
    return False

def _restart_pods() -> None:
    unique_pod: str = KUBE_POD_NAMES[0]
    if exec_check_exists(ClusterCommands.GET_PODS, unique_pod):
        print("\nRestarting ACE...")
        stop()
        return

def start_ace(ace_arguments: ACEArguments) -> None:
    first_start: bool = _create_cluster()
        
    if not ace_arguments.should_restart and not first_start:
        print(f"\nACE is already running...\n\nPlease run with {StartupArgumentsShort.RESTART} to restart!")
        return
    
    _restart_pods()

    print("\nStarting ACE...")
    time.sleep(5) # Wait for the cluster to be fully created
    start_commands: tuple[str, ...] = (ClusterCommands.EMBED_IMAGE, ClusterCommands.DEPLOY)
    _ = [execute(command) for command in start_commands]

def start_component(ace_arguments: ACEArguments) -> None:
    title: str = ace_arguments.component
    title = title.replace("_", " ").title()
    print(f"\nStarting {title}")
    match ace_arguments.component:
        case ComponentTypes.UI:
            ui.main()
        case ComponentTypes.CONTROLLER:
            controller.main()
        case ComponentTypes.QUEUE:
            queue.main()
        case ComponentTypes.MODEL_PROVIDER:
            model_provider.main()
        case ComponentTypes.SENSES:
            senses.main()
        case ComponentTypes.MEMORY:
            memory.main()
        case _:
            layer.main(ace_arguments.component)

# MAIN
def main() -> None:
    setup()
    ace_arguments: ACEArguments = assign_arguments()
    if ace_arguments.should_update:
        ace_arguments.should_build = True
        update()
    if not ace_arguments.no_build:
        ace_arguments.should_restart = True
        build(ace_arguments)
    if ace_arguments.stop:
        stop()
        return
    if ace_arguments.should_test:
        test()
        return
    if ace_arguments.component == StartupArgumentNames.STARTUP:
        start_ace(ace_arguments)
        return
    start_component(ace_arguments)

if __name__ == "__main__":
    main()
