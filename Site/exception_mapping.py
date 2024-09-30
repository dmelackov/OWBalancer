from typing import Callable
from domain.exceptions import *
from fastapi import Request
from fastapi.responses import JSONResponse

class ExceptionMap():
    def __init__(self, status_code: int, msg: str | Callable) -> None:
        self.status_code = status_code
        self.msg = msg

    def __call__(self, exception) -> tuple[int, str]:
        if isinstance(self.msg, str):
            return self.status_code, self.msg
        if isinstance(self.msg, Callable):
            return self.status_code, self.msg(exception)
        return 500, "Unkown exception message type"

exception_mapping = {
    InviteNotFoundException.__name__: ExceptionMap(404, "Invite not found"),
    InviteExpiredException.__name__: ExceptionMap(410, "Invite expired"),
    PlayerNotFoundException.__name__: ExceptionMap(404, "Player not found"),
    CantEditPlayerRolesException.__name__: ExceptionMap(403, "Not enought permission"),
    CantEditPlayerException.__name__: ExceptionMap(403, "Not enought permission"),
    PlayerAlreadyExistException.__name__: ExceptionMap(409, "Player already exist"),
    PlayerCreateException.__name__: ExceptionMap(500, "Unable to create Player"),
    PasswordDontMatchException.__name__: ExceptionMap(400, "Password dont match"),
    ProfileAlreadyExists.__name__: ExceptionMap(409, "Username already taken"),
    InvalidCredentialsException.__name__: ExceptionMap(401, "Invalid credentials"),
    WorkspaceNotFoundException.__name__: ExceptionMap(404, "Workspace not found"),
    WorkspaceCreateException.__name__: ExceptionMap(500, "Unable to create workspace"),
    RoleNotGeneratedException.__name__: ExceptionMap(500, "Roles not generated. Contact site admin"),
    RoleNotFoundException.__name__: ExceptionMap(404, "Role not found"),
    InviteCreateException.__name__: ExceptionMap(500, "Unable to create Invite"),
    DontHavePermissionException.__name__: ExceptionMap(403, "Not enought permission"),
    CantManipulateRoleException.__name__: ExceptionMap(403, "Not enought permission"),
    CantEditOtherWorkspaceProfileException.__name__: ExceptionMap(403, "Not enought permission"),
    NotParticipiantException.__name__: ExceptionMap(403, "You not participiant"),
    AlreadyParticipiantException.__name__: ExceptionMap(403, "You already participiant"),
    WorkspaceProfileNotFoundException.__name__: ExceptionMap(404, "Workspace Profile not found"),
    WorkspaceProfileCreateException.__name__: ExceptionMap(500, "Unable to create Workspace Profile")
}


async def exception_handler(request: Request, exc: Exception):
    exception_name = type(exc).__name__
    if exception_name in exception_mapping:
        status_code, message = exception_mapping[exception_name](exc)
        return JSONResponse(
            status_code=status_code,
            content={"detail": message}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Unknown error occurred"}
    )