import sys

from ci_sim._internal.cli.main import main


def _run() -> None:
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    _run()
