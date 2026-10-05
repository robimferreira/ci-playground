class CiSimError(Exception):
    """Base class for every error ci-sim raises on purpose.

    Anything that isn't a CiSimError is a bug.
    """
