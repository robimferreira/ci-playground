from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    USAGE_ERROR = 2
    LOGGING_SETUP_FAILURE = 4  # pytest reserves 3 for its own errors
    SIMULATED_ERROR = 5
