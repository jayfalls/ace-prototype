# DEPENDENCIES
## Built-in
import os
from typing import NoReturn
## Third Party
from ess_helpers.arguments import ArgumentParser
from ess_helpers import execute


# ARGUMENTS
def parse_arguments() -> NoReturn:
    os.environ["STARTUP"] = "-st/--startup" == ""

# MAIN
def main() -> NoReturn:
    print("parse args")
    startup: bool = os.environ["STARTUP"]
    if startup:
        print("venv & set requirements")
        print("build images if needed")
        print("spin up environment")
        return
    print("start a cognitive layer / utility layer based on args")

if __name__ == "__main__":
    main()
