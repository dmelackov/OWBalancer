from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependency import InviteServiceDepends, WorkspaceProfileServiceDepends
from balancer_models.models import Profile
from domain.schemes import TruncInviteInfo
from backend.exception_mapping import generate_responses_for_endpoint
from backend.utils import ProfileDepends, get_ok_response
from domain.exceptions.invite_exceptions import InviteExpiredException, InviteNotFoundException
from domain.exceptions.workspace_profile_exceptions import AlreadyParticipiantException, DontHavePermissionException, WorkspaceProfileNotFoundException
from domain.services import (InviteService, WorkspaceProfileService,
                             WorkspaceService)


router = APIRouter(
    prefix="/invite",
    tags=["invite"]
)

@router.get(
    "/{token}",
    response_model=TruncInviteInfo,
    summary="Get invite data",
    responses=generate_responses_for_endpoint([
        InviteExpiredException,
        InviteNotFoundException
    ])
)
async def get_invite_data(
    token: str,
    invite_service: InviteServiceDepends,
):
    return await invite_service.get_by_key(token)


@router.post(
    "/{token}",
    summary="Activate invite",
    responses={
        **get_ok_response("Invite sucessfully activated"),
        **generate_responses_for_endpoint([
            InviteNotFoundException,
            InviteExpiredException,
            AlreadyParticipiantException
        ])
    }
)
async def activate_invite(
    token: str,
    invite_service: InviteServiceDepends,
    profile: ProfileDepends
):
    invite = await invite_service.get_by_key(token)
    await invite_service.activate_invite(invite, profile)
    return {"message": "ok"}


@router.delete(
    "/{id}",
    summary="Deactivate invite",
    responses={
        **get_ok_response("Invite sucessfully deactivated"),
        **generate_responses_for_endpoint([
            InviteNotFoundException,
            WorkspaceProfileNotFoundException,
            DontHavePermissionException
        ])
    }
)
async def deactivate_invite(
    id: int,
    invite_service: InviteServiceDepends,
    workspace_profile_service: WorkspaceProfileServiceDepends,
    profile: ProfileDepends
):
    invite = await invite_service.get_by_id(id)
    workspace_profile = await workspace_profile_service.get_by_bind(profile, invite.creator.workspace)
    await invite_service.deactivate_invite(workspace_profile, invite)
    return {"message": "ok"}