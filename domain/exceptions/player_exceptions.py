from .domain_exception import DomainException


class PlayerNotFoundException(DomainException):
    pass


class CantEditPlayerRolesException(DomainException):
    pass


class CantEditPlayerException(DomainException):
    pass


class PlayerAlreadyExistException(DomainException):
    pass


class PlayerCreateException(DomainException):
    pass
