from app.DataBase.db import *
import secrets
from app.Static.globalClasses import AnswerForm


def createWorkspace(U, Name, WorkspaceParams):
    W = Workspace.select().where(Workspace.Name == Name)
    if W:
        return AnswerForm(status=False, error="already_exist")

    W = Workspace.create(Creator=U, Name=Name, WorkspaceParams=WorkspaceParams)
    return AnswerForm(status=True, error=None, data=W)


def deleteWorkspace(WID):
    W = Workspace.select().where(Workspace.ID == WID)
    if W:
        W[0].delete_instance()
        return AnswerForm(status=True, error=None)
    else:
        return AnswerForm(status=False, error="instance_not_exist")


def createInvite(U, W, UseLimit=1):
    Key = W.ID + secrets.token_urlsafe(8)
    while KeyData.select().where(KeyData.Key == Key):
        Key = W.ID + secrets.token_urlsafe(8)
    KD = KeyData.create(Key=Key, Workspace=Workspace, Creator=U, UseLimit=UseLimit)
    return AnswerForm(status=True, error=None, data=KD)


def joinWorkspace(U, W, InviteKey):
    KD = KeyData.select().where(KeyData.Key == InviteKey)
    if not KD:
        return AnswerForm(status=False, error="invalid_key")

    WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U and WorkspaceProfile.Workspace == W)
    if WU:
        return AnswerForm(status=False, error="already_in")

    KD = KD[0]
    if KD.UseLimit > 0:
        KD.UseLimit -= 1
    elif KD.UseLimit == 0:
        return AnswerForm(status=False, error="use_limit")

    WU = WorkspaceProfile.create(Profile=U, Workspace=W)
    return AnswerForm(status=True, error=None, data=WU)


def getWorkspaceProfile(U, W):
    WU = WorkspaceProfile.select().where(WorkspaceProfile.Profile == U, WorkspaceProfile.Workspace == W)
    if WU:
        return AnswerForm(status=True, error=None, data=WU[0])
    else:
        return AnswerForm(status=False, error="instance_not_exist")


