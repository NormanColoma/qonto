from domain.common.application_error import ApplicationError


class InvalidIbanError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
