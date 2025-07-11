from tkinter import W
from typing import Annotated
from fastapi import Depends, FastAPI, Request

from balancer_models.repository.custom_repository import CustomRepository
from balancer_models.repository.invite_repository import InviteRepository
from balancer_models.repository.lobby_repository import LobbyRepository
from balancer_models.repository.permission_repository import PermissionRepository
from balancer_models.repository.player_repository import PlayerRepository
from balancer_models.repository.profile_repository import ProfileRepository
from balancer_models.repository.role_repository import RoleRepository
from balancer_models.repository.workspace_profile_repository import WorkspaceProfileRepository
from balancer_models.repository.workspace_repository import WorkspaceRepository
from domain.services.custom_service import CustomService
from domain.services.invite_service import InviteService
from domain.services.player_service import PlayerService
from domain.services.profile_service import ProfileService
from domain.services.workspace_profile_service import WorkspaceProfileService
from domain.services.workspace_service import WorkspaceService
from infrastructure.database import DatabaseSessionManager
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session(request: Request):
    session_manager: DatabaseSessionManager = request.app.state.session_manager
    session_generator = session_manager.session()
    async for session in session_generator:
        yield session
    

DB_SESSION = Annotated[AsyncSession, Depends(get_db_session)]


async def get_custom_repository(session: DB_SESSION):
    return CustomRepository(session)


async def get_invite_repository(session: DB_SESSION):
    return InviteRepository(session)


async def get_lobby_repository(session: DB_SESSION):
    return LobbyRepository(session)


async def get_permission_repository(session: DB_SESSION):
    return PermissionRepository(session)


async def get_player_repository(session: DB_SESSION):
    return PlayerRepository(session)


async def get_profile_repository(session: DB_SESSION):
    return ProfileRepository(session)


async def get_workspace_repository(session: DB_SESSION):
    return WorkspaceRepository(session)


async def get_workspace_profile_repository(session: DB_SESSION):
    return WorkspaceProfileRepository(session)


async def get_role_repository(session: DB_SESSION):
    return RoleRepository(session)

CustomRepositoryDepends = Annotated[CustomRepository, Depends(
    get_custom_repository)]
InviteRepositoryDepends = Annotated[InviteRepository, Depends(
    get_invite_repository)]
LobbyRepositoryDepends = Annotated[LobbyRepository, Depends(
    get_lobby_repository)]
PermissionRepositoryDepends = Annotated[PermissionRepository, Depends(
    get_permission_repository)]
PlayerRepositoryDepends = Annotated[PlayerRepository, Depends(
    get_player_repository)]
ProfileRepositoryDepends = Annotated[ProfileRepository, Depends(
    get_profile_repository)]
WorkspaceRepositoryDepends = Annotated[WorkspaceRepository, Depends(
    get_workspace_repository)]
WorkspaceProfileRepositoryDepends = Annotated[WorkspaceProfileRepository, Depends(
    get_workspace_profile_repository)]
RoleRepositoryDepends = Annotated[RoleRepository, Depends(get_role_repository)]


async def get_player_service(player_repository: PlayerRepositoryDepends,
                             workspace_profile_service: WorkspaceProfileService):
    return PlayerService(workspace_profile_service,
                         player_repository)


async def get_profile_service(profile_repository: ProfileRepositoryDepends):
    return ProfileService(profile_repository)


async def get_workspace_service(workspace_repository: WorkspaceRepositoryDepends,
                                workspace_profile_repository: WorkspaceProfileRepositoryDepends,
                                role_repository: RoleRepositoryDepends,
                                invite_repository: InviteRepositoryDepends,
                                lobby_repository: LobbyRepositoryDepends):
    return WorkspaceService(role_repository,
                            workspace_repository,
                            workspace_profile_repository,
                            invite_repository,
                            lobby_repository)


async def get_workspace_profile_service(role_repository: RoleRepositoryDepends,
                                        workspace_repository: WorkspaceRepositoryDepends,
                                        workspace_profile_repository: WorkspaceProfileRepositoryDepends,
                                        lobby_repository: LobbyRepositoryDepends):
    return WorkspaceProfileService(role_repository,
                                   workspace_repository,
                                   workspace_profile_repository,
                                   lobby_repository)


WorkspaceServiceDepends = Annotated[WorkspaceService, Depends(
    get_workspace_service)]
WorkspaceProfileServiceDepends = Annotated[WorkspaceProfileService, Depends(
    get_workspace_profile_service)]


async def get_invite_service(workspace_profile_service: WorkspaceProfileServiceDepends,
                             invite_repository: InviteRepositoryDepends,
                             workspace_service: WorkspaceServiceDepends):
    return InviteService(workspace_service,
                         workspace_profile_service,
                         invite_repository)


async def get_custom_service(workspace_profile_service: WorkspaceProfileServiceDepends,
                             workspace_service: WorkspaceServiceDepends):
    return CustomService(workspace_service,
                         workspace_profile_service)

PlayerServiceDepends = Annotated[PlayerService, Depends(get_player_service)]
ProfileServiceDepends = Annotated[ProfileService, Depends(get_profile_service)]
InviteServiceDepends = Annotated[InviteService, Depends(get_invite_service)]
CustomServiceDepends = Annotated[CustomService, Depends(get_custom_service)]
