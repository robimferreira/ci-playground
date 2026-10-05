class CiSimError(Exception):
    """Base exception for all ci_sim errors."""

    def __init__(self, message: str, exit_code: int = 1):
        self.message = message
        self.exit_code = exit_code
        super().__init__(self.message)


class ConfigurationError(CiSimError):
    pass


class NetworkError(CiSimError):
    pass


class ValidationErrr(CiSimError):
    pass
