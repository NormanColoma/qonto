from domain.common.application_error import ApplicationError


class InsufficientFundsError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
