from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.status import HTTP_404_NOT_FOUND

from app.DataBase.db import Profile, WorkspaceProfile, Workspace
from app.Site.loginManager import manager
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


@router.get("/getWorkspaces/")
async def getWorkspaces(user: Profile = Depends(manager)):
    workspaces = user.getWorkspaceList().data
    return [i.getJson() for i in workspaces]


@router.get("/getWorkspace/{workspaceID}")
async def getWorkspaces(workspaceID: int, user: Profile = Depends(manager)):
    workspace = Workspace.getInstance(workspaceID)
    if workspace is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    workspaceProfile = WorkspaceProfile.getWU(user, workspace).data
    if workspaceProfile is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
    return workspace.getJson()
