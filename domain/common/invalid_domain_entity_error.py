from domain.common.application_error import ApplicationError


class InvalidDomainEntityError(ApplicationError):
    def __init__(self, message):
        super().__init__(message)
