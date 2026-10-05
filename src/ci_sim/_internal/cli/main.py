"""command-line entry point (`ci-sim`, declared in [project.scripts])."""

from __future__ import annotations

import argparse
import logging
import signal
import sys
import time
import uuid
from collections.abc import Sequence
from types import FrameType
from typing import Final

from ci_sim import DESCRIPTION, DIST_NAME, __version__
from ci_sim._internal.cli.exit_codes import ExitCode
from ci_sim._internal.exceptions import ConfigurationError, Terminated
from ci_sim._internal.utils.logging import run_id_var, setup_logging

log: Final = logging.getLogger(__name__)

VERBOSITY: Final[tuple[str | None, ...]] = (None, "INFO", "DEBUG")


def _on_sigterm(signum: int, _frame: FrameType | None) -> None:
    raise Terminated(signal.Signals(signum).name)


def main(argv: Sequence[str] | None = None) -> ExitCode:
    parser = argparse.ArgumentParser(
        prog=DIST_NAME,
        description=DESCRIPTION,
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
    except ConfigurationError as exc:
        # logging isn't configured up to this point, so print instead of log
        print(f"{parser.prog}: error: {exc}", file=sys.stderr)
        return ExitCode.USAGE_ERROR

    signal.signal(signal.SIGTERM, _on_sigterm)
    started = time.monotonic()

    try:
        run_id_var.set(uuid.uuid4().hex)
        log.info("%s started", DIST_NAME, extra={"event": "run.started"})
        time.sleep(7)
        log.info("%s finished", DIST_NAME, extra={"event": "run.finished"})
        return ExitCode.SUCCESS
    except (KeyboardInterrupt, Terminated) as exc:
        name: str = "SIGINT" if isinstance(exc, KeyboardInterrupt) else str(exc)
        log.warning(
            "run interrupted by %s",
            name,
            extra={
                "event": "run.interrupted",
                "signal": name,
                "duration_s": round(
                    number=(time.monotonic() - started), ndigits=3
                ),
            },
        )
        return ExitCode.INTERRUPTED if name == "SIGINT" else ExitCode.TERMINATED
