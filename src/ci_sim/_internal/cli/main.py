"""command-line entry point (`ci-sim`, declared in [project.scripts])."""

from __future__ import annotations

import argparse
import logging
import sys
import uuid
from collections.abc import Sequence
from time import sleep
from typing import Final

from ci_sim import DIST_NAME, __version__
from ci_sim._internal.cli.exit_codes import ExitCode
from ci_sim._internal.utils.logging import run_id_var, setup_logging

log: Final = logging.getLogger(__name__)

VERBOSITY: Final[tuple[str | None, ...]] = (None, "INFO", "DEBUG")


def main(argv: Sequence[str] | None = None) -> ExitCode:
    parser = argparse.ArgumentParser(
        prog=f"{DIST_NAME}",
        description="Simulate CI events.",
    )
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="-v info, -vv debug"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args(argv)
    verbose: int = args.verbose

    try:
        setup_logging(VERBOSITY[min(verbose, 2)])
    except ValueError as exc:
        # logging isn't configured up to this point
        print(f"ci_sim: {exc}", file=sys.stderr)
        return ExitCode.LOGGING_SETUP_FAILURE

    run_id_var.set(uuid.uuid4().hex[:12])
    log.info(f"{DIST_NAME} started")
    sleep(1)
    print(f"Run {run_id_var.get()} is printing stuff to stdout :D")
    sleep(2)
    log.info(f"{DIST_NAME} finished")
    return ExitCode.SUCCESS
