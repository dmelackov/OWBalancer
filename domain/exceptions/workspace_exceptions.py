from .domain_exception import DomainException


class WorkspaceNotFoundException(DomainException):
    pass

class WorkspaceCreateException(DomainException):
    pass

class RoleNotGeneratedException(DomainException):
    pass

class RoleNotFoundException(DomainException):
    pass

class InviteCreateException(DomainException):
    pass