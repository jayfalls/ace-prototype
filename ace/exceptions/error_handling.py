# DEPENDENCIES
## Built-in
import sys


# FUNCTIONS
def exit_on_error(error: str) -> None:
    print(f"ERROR: {error}")
    sys.exit(1)