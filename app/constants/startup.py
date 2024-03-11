# DEPENDENCIES
## Built-in
import os


class StartupCommands:
    UPDATE: str = "git pull"


# COMPONENTS
class ComponentTypes:
    CONTROLLER: str = "controller"
    QUEUE: str = "queue"
    SENSES: str = "senses"
    MEMORY: str = "memory"
    ASPIRATIONAL: str = "aspirational"
    GLOBAL_STRATEGY: str = "global-strategy"
    AGENT_MODEL: str = "agent-model"
    EXECUTIVE_FUNCTION: str = "executive-function"
    COGNITIVE_CONTROL: str = "cognitive-control"
    TASK_PROSECUTION: str = "task-prosecution"

COMPONENT_TYPES: tuple = (
    ComponentTypes.CONTROLLER,
    ComponentTypes.QUEUE,
    ComponentTypes.SENSES,
    ComponentTypes.MEMORY,
    ComponentTypes.ASPIRATIONAL,
    ComponentTypes.GLOBAL_STRATEGY,
    ComponentTypes.AGENT_MODEL,
    ComponentTypes.EXECUTIVE_FUNCTION,
    ComponentTypes.COGNITIVE_CONTROL,
    ComponentTypes.TASK_PROSECUTION
)


# ARGUMENTS
class StartupArgumentNames:
    DEBUG: str = "debug"
    TEST: str = "test"
    BUILD: str = "build"
    NO_BUILD: str = "no_build"
    LOCAL: str = "local"
    STARTUP: str = "startup"
    STOP: str = "stop"
    RESTART: str = "restart"
    UPDATE: str = "update"
    COMPONENT_TYPE: str = "component_type"

STARTUP_BOOL_ARGUMENTS: tuple[str, ...] = (
    StartupArgumentNames.DEBUG,
    StartupArgumentNames.TEST,
    StartupArgumentNames.BUILD,
    StartupArgumentNames.NO_BUILD,
    StartupArgumentNames.LOCAL,
    StartupArgumentNames.STOP,
    StartupArgumentNames.RESTART,
    StartupArgumentNames.UPDATE
)

STARTUP_STRING_ARGUMENTS: tuple[str, ...] = (
    StartupArgumentNames.COMPONENT_TYPE,
)

STARTUP_ARGUMENTS: dict[str, frozenset] = {
    StartupArgumentNames.DEBUG: frozenset(("-d", "--debug")),
    StartupArgumentNames.TEST: frozenset(("-t", "--test")),
    StartupArgumentNames.BUILD: frozenset(("-b", "--build")),
    StartupArgumentNames.NO_BUILD: frozenset(("-nb", "--no-build")),
    StartupArgumentNames.LOCAL: frozenset(("-l", "--local")),
    StartupArgumentNames.STOP: frozenset(("-s", "--stop")),
    StartupArgumentNames.RESTART: frozenset(("-r", "--restart")),
    StartupArgumentNames.UPDATE: frozenset(("-u", "--update")),
    StartupArgumentNames.COMPONENT_TYPE: frozenset(("-ct", "--component-type"))
}

class StartupArgumentsShort:
    DEBUG: str = "-d"
    TEST: str = "-t"
    BUILD: str = "-b"
    NO_BUILD: str = "-nb"
    LOCAL: str = "-l"
    STOP: str = "-s"
    RESTART: str = "-r"
    UPDATE: str = "-u"
    COMPONENT_TYPE: str = "-ct"

STARTUP_ARGUMENTS_HELP: dict[str, str] = {
    StartupArgumentNames.DEBUG: "Enable debug mode",
    StartupArgumentNames.TEST: "Run tests",
    StartupArgumentNames.BUILD: "Build the images",
    StartupArgumentNames.NO_BUILD: "Skip the build",
    StartupArgumentNames.LOCAL: "Run in local mode for development purposes",
    StartupArgumentNames.STOP: "Stop the ACE cluster",
    StartupArgumentNames.RESTART: "Restart the ACE cluster",
    StartupArgumentNames.UPDATE: "Update the ACE",
    StartupArgumentNames.COMPONENT_TYPE: f"Select the component type. Available types: {', '.join(COMPONENT_TYPES)}"
}


# CONTAINERS
_SETUP_FOLDER: str = "./setup"

## Image
ACE_IMAGE_NAME: str = "ace_prototype"
_FULL_ACE_IMAGE_NAME: str = f"localhost/{ACE_IMAGE_NAME}:latest"

class ImageCommands:
    CHECK_IMAGES: str = "podman images"
    BUILD_IMAGE: str = f"podman build -t {ACE_IMAGE_NAME}  -f {_SETUP_FOLDER}/Containerfile ."

## Volumes
class VolumePaths:
    STORAGE_PATH: str = "storage"
    HOST_PATH: str = f"{os.getcwd()}/{STORAGE_PATH}"
    HOST_CONTROLLER: str = f"{HOST_PATH}/controller"
    HOST_OUTPUT: str = f"{HOST_PATH}/output"
    CONTAINER_PATH: str = f"/home/ace/{STORAGE_PATH}"
    CONTROLLER: str = f"{CONTAINER_PATH}/controller"
    OUTPUT: str = f"{CONTAINER_PATH}/output"

class DevVolumePaths:
    STORAGE_PATH: str = "./.storage"
    CONTROLLER_STORAGE_PATH: str = f"{STORAGE_PATH}/controller"
    CONTROLLER_SETTINGS_PATH: str = f"{CONTROLLER_STORAGE_PATH}/settings"
    OUTPUT_STORAGE_PATH: str = f"{STORAGE_PATH}/output"

## Network
ACE_NETWORK_NAME: str = "ace-network"

class NetworkCommands:
    CHECK_NETWORK: str = "podman network ls"
    CREATE_NETWORK: str = f"podman network create {ACE_NETWORK_NAME}"

## Deployment
ACE_POD_NAME: str = "ace"

class DeploymentFile: 
    PATH: str = f"{_SETUP_FOLDER}/deployment.yaml"
    USER_PATH: str = f"{_SETUP_FOLDER}/.user_deployment.yaml"

class DeploymentCommands:
    CHECK: str = "podman pod ps"
    _DEPLOY_COMMAND: str = "podman kube play"
    DEPLOY: str = f"{_DEPLOY_COMMAND} --network {ACE_NETWORK_NAME} --replace {DeploymentFile.USER_PATH}"
    STOP: str = f"{_DEPLOY_COMMAND} --network {ACE_NETWORK_NAME} --down {DeploymentFile.USER_PATH}"

DEPLOYMENT_REPLACE_KEYWORDS: dict[str, str] = {
    "{{ ace_pod_name }}": ACE_POD_NAME,
    "{{ ace_image_name }}": _FULL_ACE_IMAGE_NAME,
    "{{ start_command }}": """python3\n    - main.py\n    - -nb\n    - -ct""",
    "{{ controller_host_path }}": VolumePaths.HOST_CONTROLLER,
    "{{ controller_container_path }}": VolumePaths.CONTROLLER,
    "{{ output_host_path }}": VolumePaths.HOST_OUTPUT,
    "{{ output_container_path }}": VolumePaths.OUTPUT
}
