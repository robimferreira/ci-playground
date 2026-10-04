"""command-line entry point (`ci-sim`, declared in [project.scripts])."""

from __future__ import annotations

import argparse
import logging
import sys
import uuid
from collections.abc import Sequence
from time import sleep
from typing import Final

from ci_sim import __version__
from ci_sim.logging_config import run_id_var, setup_logging

log: Final = logging.getLogger(__name__)

VERBOSITY: Final[tuple[str | None, ...]] = (None, "INFO", "DEBUG")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ci-sim",
        description="adsadsadsa.",
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
        return 2

    run_id_var.set(uuid.uuid4().hex[:12])
    log.info("ci_sim started")
    sleep(1)
    log.info("ci_sim finished")
    return 0
