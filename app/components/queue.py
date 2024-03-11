# DEPENDENCIES
## Local
from constants.queue import Queue
from helpers import execute

# MAIN
def main() -> None:
    print("Starting Queue")
    execute(Queue.START)