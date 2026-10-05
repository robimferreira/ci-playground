"""ci-sim: a generic workflow of a ci tool"""

from importlib.metadata import metadata
from typing import Final

# ssot: version in pyproject.toml
DIST_NAME: Final = "ci-sim"
_METADATA: Final = metadata(DIST_NAME)
__version__: Final = _METADATA["Version"]
DESCRIPTION: Final = _METADATA["Summary"]
