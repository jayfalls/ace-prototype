#!/usr/bin/env python3
"""
Starting point for the ACE Prototype, as well as the individual components.

Author: jayfalls

Arguments:
    -d/--debug: bool -> Enable debug mode
    -t/--test: bool -> Run tests
    -b/--build: bool -> Build the images
    -nb/--no-build: bool -> Skip the build check
    -l/--local: bool -> Run in local for development
    -s/--stop: bool -> Stop the ACE cluster
    -r/--restart: bool -> Restart the ACE cluster deployment
    -u/--update: bool -> Update the ACE
    -ct/--component-type: str -> The type of this component
"""


# DEPENDENCIES
## Built-in
from argparse import ArgumentParser
import os
## Third Party
import pytest
## Local
from config import DebugSettings
from constants.settings import DebugLevels
from constants.startup import (
    StartupCommands, ComponentTypes, COMPONENT_TYPES, 
    StartupArgumentNames, STARTUP_BOOL_ARGUMENTS, STARTUP_STRING_ARGUMENTS, STARTUP_ARGUMENTS, STARTUP_ARGUMENTS_HELP,
    StartupArgumentsShort,
    ACE_IMAGE_NAME, ImageCommands, 
    VolumePaths, ACE_NETWORK_NAME, NetworkCommands,
    DeploymentFile, DEPLOYMENT_REPLACE_KEYWORDS, ACE_POD_NAME, DeploymentCommands
)
from components import (
    controller, queue, senses, memory, layer
)
from exceptions.error_handling import exit_on_error
from helpers import debug_print, execute, exec_check_exists


# VARIABLES
class ACEArguments:
    debug: bool = False
    should_test: bool = False
    should_build: bool = False
    no_build: bool = False
    local_mode: bool = False
    stop: bool = False
    should_restart: bool = False
    should_update: bool = False
    component: str = ""


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
    ace_arguments.local_mode = arguments.get(StartupArgumentNames.LOCAL, False)
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
def build(request_build: bool) -> bool:
    print("\nChecking if build is required...")
    check_images_command: str = ImageCommands.CHECK_IMAGES
    image_exists: bool = exec_check_exists(check_images_command, ACE_IMAGE_NAME)
    should_build: bool = not image_exists or request_build
    if should_build:
        if not image_exists:
            print("\nImage does not exist\nBuilding container...")
        else:
            print("\nBuilding container...")
        build_ace_images_command: str = ImageCommands.BUILD_IMAGE
        execute(build_ace_images_command, error_message="Unable to build image")
        return should_build
    print("\nImage already exists\nSkipping build...")
    return should_build


# SETUP
def _setup_folders(local_mode: bool) -> None:
    if not local_mode:
        required_paths: tuple[str, ...] = (VolumePaths.HOST_CONTROLLER, VolumePaths.HOST_OUTPUT)
        _ = [os.makedirs(dir_path, exist_ok=True) for dir_path in required_paths]

def _setup_user_deployment_file() -> None:
    if os.path.isfile(DeploymentFile.USER_PATH):
        return
    print("\nFirst time setting up user deployment file...")
    with open(DeploymentFile.PATH, "r", encoding="utf-8") as deployment_file:
        deployment_string: str = deployment_file.read()
        deployment_file.close()
    for key, replace in DEPLOYMENT_REPLACE_KEYWORDS.items():
        deployment_string = deployment_string.replace(key, replace)
    with open(DeploymentFile.USER_PATH, "w", encoding="utf-8") as user_deployment_file:
        user_deployment_file.write(deployment_string)
        user_deployment_file.close()

def setup(local_mode: bool) -> None:
    _setup_folders(local_mode)
    _setup_user_deployment_file()


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
    update_command: str = StartupCommands.UPDATE
    execute(update_command)

def _setup_network() -> None:
    if not exec_check_exists(NetworkCommands.CHECK_NETWORK, ACE_NETWORK_NAME):
        print("\nFirst time setting up network...")
        execute(NetworkCommands.CREATE_NETWORK)

def stop(exists: bool) -> None:
    if not exists:
        print("ACE is not running! Cannot stop...")
        return
    print("\nStopping ACE...")
    execute(DeploymentCommands.STOP)

def start_ace(restart: bool, exists: bool) -> None:
    deploy_command: str = DeploymentCommands.DEPLOY
    if restart:
        print("\nRestarting ACE...")
        execute(deploy_command)
        return
    if exists:
        print(f"\nACE is already running...\n\nPlease run with {StartupArgumentsShort.RESTART} to restart!")
        return
    print("\nStarting ACE...")
    execute(deploy_command)      

def start_component(title: str, local_mode: bool) -> None:
    print_title = title.replace("_", " ").title()
    print(f"\nStarting {print_title}")
    match title:
        case ComponentTypes.CONTROLLER:
            controller.main(local_mode=local_mode)
        case ComponentTypes.QUEUE:
            queue.main()
        case ComponentTypes.SENSES:
            senses.main()
        case ComponentTypes.MEMORY:
            memory.main()
        case _:
            layer.main(title)

# MAIN
def main() -> None:
    ace_arguments: ACEArguments = assign_arguments()
    setup(ace_arguments.local_mode)
    if ace_arguments.should_update:
        ace_arguments.should_build = True
        update()
    if not ace_arguments.no_build:
        built: bool = build(ace_arguments.should_build)
        if built:
            ace_arguments.should_restart = True
    if ace_arguments.should_test:
        test()
        return
    if not ace_arguments.component == StartupArgumentNames.STARTUP:
        start_component(ace_arguments.component, ace_arguments.local_mode)
        return
    exists: bool = exec_check_exists(DeploymentCommands.CHECK, ACE_POD_NAME)
    if ace_arguments.stop:
        stop(exists)
        return
    _setup_network()
    start_ace(ace_arguments.should_restart, exists)
    

if __name__ == "__main__":
    main()
