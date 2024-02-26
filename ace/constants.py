# SETTINGS
class DebugLevels:
    ERROR: int = 0
    WARNING: int = 1
    INFO: int = 2
    DEBUG: int = 3

# STARTUP
class Commands:
    UPDATE_COMMAND: str = "git pull"

## Components
class ComponentTypes:
    UI: str = "ui"
    CONTROLLER: str = "controller"
    QUEUE: str = "queue"
    MODEL_PROVIDER: str = "model_provider"
    SENSES: str = "senses"
    MEMORY: str = "memory"
    ASPIRATIONAL: str = "aspirational"
    GLOBAL_STRATEGY: str = "global_strategy"
    AGENT_MODEL: str = "agent_model"
    EXECUTIVE_FUNCTION: str = "executive_function"
    COGNITIVE_CONTROL: str = "cognitive_control"
    TASK_PROSECUTION: str = "task_prosecution"

COMPONENT_TYPES: tuple = (
    ComponentTypes.UI,
    ComponentTypes.CONTROLLER,
    ComponentTypes.QUEUE,
    ComponentTypes.MODEL_PROVIDER,
    ComponentTypes.SENSES,
    ComponentTypes.MEMORY,
    ComponentTypes.ASPIRATIONAL,
    ComponentTypes.GLOBAL_STRATEGY,
    ComponentTypes.AGENT_MODEL,
    ComponentTypes.EXECUTIVE_FUNCTION,
    ComponentTypes.COGNITIVE_CONTROL,
    ComponentTypes.TASK_PROSECUTION
)

## Arguments
class StartupArgumentNames:
    DEBUG: str = "debug"
    TEST: str = "test"
    BUILD: str = "build"
    NO_BUILD: str = "no_build"
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
    STOP: str = "-s"
    RESTART: str = "-r"
    UPDATE: str = "-u"
    COMPONENT_TYPE: str = "-ct"

STARTUP_ARGUMENTS_HELP: dict[str, str] = {
    StartupArgumentNames.DEBUG: "Enable debug mode",
    StartupArgumentNames.TEST: "Run tests",
    StartupArgumentNames.BUILD: "Build the images",
    StartupArgumentNames.NO_BUILD: "Skip the build",
    StartupArgumentNames.STOP: "Stop the ACE cluster",
    StartupArgumentNames.RESTART: "Restart the ACE cluster",
    StartupArgumentNames.UPDATE: "Update the ACE",
    StartupArgumentNames.COMPONENT_TYPE: f"Select the component type. Available types: {', '.join(COMPONENT_TYPES)}"
}

## Image
ACE_IMAGE_NAME: str = "ace_prototype"

class ImageCommands:
    CHECK_IMAGES: str = "docker images"
    BUILD_IMAGE: str = f"docker build -t {ACE_IMAGE_NAME}  -f ./setup/Dockerfile ."

## Cluster
CLUSTER_NAME: str = "ACE"

KUBE_POD_NAMES: tuple[str, ...] = (
   "interface",
   "layers",
   "llm",
   "queue"
)

KUBE_SERVICE_NAMES: tuple[str, ...] = (
    "ui",
    "controller",
    "llm",
    "queue"
)

class ClusterCommands:
    GET_PODS: str = "kubectl get pods"
    DELETE_POD: str = "kubectl delete pod"
    DELETE_SERVICE: str = "kubectl delete service"
    GET_CLUSTER: str = "k3d cluster list"
    CREATE_CLUSTER: str = f"k3d cluster create {CLUSTER_NAME}"
    APPLY_CONFIG: str = "kubectl apply -f setup/create_cluster.yaml"
    EMBED_IMAGE: str = f"k3d image import {ACE_IMAGE_NAME}:latest -c {CLUSTER_NAME}"
    DEPLOY: str = "kubectl apply -f setup/deployment.yaml"

class VolumePaths:
    HOST_CONTROLLER: str = "./storage/controller"
    HOST_OUTPUT: str = "./storage/output"
    CONTROLLER: str = "/home/ace/controller"
    OUTPUT: str = "/home/ace/output"

