import sys

from ci_sim._internal.cli.exit_codes import ExitCode
from ci_sim._internal.cli.main import main


def _run() -> ExitCode:
    try:
        return main()
    except KeyboardInterrupt:
        return ExitCode.INTERRUPTED


if __name__ == "__main__":
    sys.exit(_run())
