from enum import IntEnum


class ExitCode(IntEnum):
    SUCCESS = 0
    INTERNAL_ERROR = 1
    USAGE_ERROR = 2
    INTERRUPTED = 130
    TERMINATED = 143
