"""ci-sim: a generic workflow of a ci tool"""

from importlib.metadata import version
from typing import Final

DIST_NAME: Final = "ci-sim"
__version__: Final = version(DIST_NAME)  # ssot: version in pyproject.tml
