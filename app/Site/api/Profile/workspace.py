from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND)

import app.DataBase.dataModels as dataModels
from app.DataBase.db import (KeyData, Profile, Roles, Workspace,
                             WorkspaceProfile)
from app.DataBase.permissions import Permissions
from app.Site.loginManager import manager
from app.Site.utils import getWorkspaceProfile

router = APIRouter(
    prefix="/workspace",
    tags=["workspace"]
)


@router.put("/setWorkspace/{workspaceID}")
async def setWorkspace(response: Response, workspaceID: int, user: Profile = Depends(manager)):
    workspace = Workspace.getInstance(workspaceID)
    if workspace is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    workspaceProfile = WorkspaceProfile.getWU(user, workspace).data
    if workspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    response.set_cookie("workspace", str(workspace.ID), max_age=60*60*24*30)
    return {"message": "OK"}


@router.get("/getWorkspaces")
async def getWorkspaces(user: Profile = Depends(manager)) -> list[dataModels.Workspace]:
    workspaces = user.getWorkspaceList().data
    return [i.getJson() for i in workspaces]


@router.get("/getWorkspace/{workspaceID}")
async def getWorkspace(workspaceID: int, user: Profile = Depends(manager)) -> dataModels.Workspace:
    workspace = Workspace.getInstance(workspaceID)
    if workspace is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    workspaceProfile = WorkspaceProfile.getWU(user, workspace).data
    if workspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    return workspace.getJson()


class CreateWorkspaceParams(BaseModel):
    CustomSystem: bool


class CreateWorkspaceRequest(BaseModel):
    name: str
    params: CreateWorkspaceParams


@router.post("/createWorkspace")
async def createWorkspace(req: CreateWorkspaceRequest, user: Profile = Depends(manager)):
    workspace = Workspace.create(
        user, req.name, req.params.model_dump_json()).data
    role = Roles.getRole("Administrator")
    if role.data is None:
        return {"error": role.error}
    workspaceProfile = WorkspaceProfile.create(user, workspace).data
    workspaceProfile.setRole(role.data)
    return {"message": "OK"}


class ActivateInviteCodeRequest(BaseModel):
    keyCode: str


@router.post("/activateInviteCode")
async def activateInviteCode(req: ActivateInviteCodeRequest, user: Profile = Depends(manager)):
    keyData = KeyData.getByKey(req.keyCode).data
    if not keyData:
        raise HTTPException(HTTP_404_NOT_FOUND, "Invite not found")
    joinStatus = keyData.Workspace.joinWorkspace(user, keyData)
    if not joinStatus.status:
        raise HTTPException(HTTP_404_NOT_FOUND, joinStatus.error)
    return {"message": "OK"}


@router.post("/getInviteCodeInfo/{code}")
async def getInviteCodeInfo(code: str, user: Profile = Depends(manager)):
    keyData = KeyData.getByKey(code).data
    if not keyData:
        raise HTTPException(HTTP_404_NOT_FOUND, "Invite not found")
    if keyData.UseLimit == 0:
        raise HTTPException(HTTP_404_NOT_FOUND, "Invite not found")
    return keyData.getJson()


class ChangeWorkspaceUserRoleRequest(BaseModel):
    userID: int
    roleID: int


@router.post("/changeWorkspaceUserRole")
async def changeWorkspaceUserRole(req: ChangeWorkspaceUserRoleRequest, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.moderate_workspace):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    targetWorkspaceProfile = WorkspaceProfile.getInstance(req.userID)
    if targetWorkspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found profile")
    role = Roles.getInstance(req.roleID)
    if role is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found role")
    if targetWorkspaceProfile.Workspace.ID != workspaceProfile.Workspace.ID:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    if targetWorkspaceProfile.Role.ID >= workspaceProfile.Role.ID:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    targetWorkspaceProfile.setRole(role)
    return {"message": "OK"}


class ChangeKickWorkspaceUser(BaseModel):
    userID: int


@router.post("/kickWorkspaceUser")
async def kickWorkspaceUser(req: ChangeKickWorkspaceUser, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    if not workspaceProfile.checkPermission(Permissions.moderate_workspace):
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    targetWorkspaceProfile = WorkspaceProfile.getInstance(req.userID)
    if targetWorkspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Not found profile")
    if targetWorkspaceProfile.Workspace.ID != workspaceProfile.Workspace.ID:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    if targetWorkspaceProfile.Role.ID >= workspaceProfile.Role.ID:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")
    targetWorkspaceProfile.Active = False
    targetWorkspaceProfile.save()
    return {"message": "OK"}


@router.post("/leaveFromWorkspace")
async def leaveFromWorkspace(res: Response, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)):
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    workspaceProfile.Active = False
    workspaceProfile.save()
    res.set_cookie("access-token", "", max_age=0, httponly=True)
    return {"message": "OK"}

@router.get("/getWorkspaceMembers")
async def leaveFromWorkspace(res: Response, workspaceProfile: WorkspaceProfile | None = Depends(getWorkspaceProfile)) -> list[dataModels.WorkspaceProfile]:
    if workspaceProfile is None:
        raise HTTPException(HTTP_401_UNAUTHORIZED,
                            "Not found workspace profile")
    return [i.getJson() for i in workspaceProfile.Workspace.getWorkspaceMembers()]