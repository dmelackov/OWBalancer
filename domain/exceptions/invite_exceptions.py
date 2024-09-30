from .domain_exception import DomainException

class InviteNotFoundException(DomainException):
    pass

class InviteExpiredException(DomainException):
    pass