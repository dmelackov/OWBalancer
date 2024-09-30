from .domain_exception import DomainException

class DontHavePermissionException(DomainException):
    def __init__(self, permission: str, *args: object) -> None:
        super().__init__(*args)
        self.permission = permission

class CantManipulateRoleException(DomainException):
    pass

class CantEditOtherWorkspaceProfileException(DomainException):
    pass

class NotParticipiantException(DomainException):
    pass

class AlreadyParticipiantException(DomainException):
    pass

class WorkspaceProfileNotFoundException(DomainException):
    pass

class WorkspaceProfileCreateException(DomainException):
    pass