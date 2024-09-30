from .domain_exception import DomainException

class PasswordDontMatchException(DomainException):
    pass

class ProfileAlreadyExists(DomainException):
    pass

class InvalidCredentialsException(DomainException):
    pass