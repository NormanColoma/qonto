from domain.common.application_error import ApplicationError


class InvalidTransferOperationError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
