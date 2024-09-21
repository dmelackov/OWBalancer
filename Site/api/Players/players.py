from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import (HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from DataBase.database import get_db_session
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.models.player import Player
from DataBase.permissions import Permissions
from DataBase.repository.player_repository import PlayerRepository
from DataBase.repository.role_repository import RoleRepository
from DataBase.schemes.player import PlayerBaseScheme, PlayerScheme
from Site.utils import get_workspace_profile


from fastapi_controllers import Controller, post, get, delete, patch


router = APIRouter(
    prefix="/players",
    tags=["players"]
)


class CreatePlayerRequest(BaseModel):
    username: str


class PatchPlayerRequest(BaseModel):
    username: Optional[str] = None
    is_flex: Optional[bool] = None
    roles: Optional[Annotated[str, Query(
        pattern="^[TDH]?[TDH]?[TDH]?$")]] = None


class PlayerController(Controller):
    prefix = "/players"
    tags = ["players"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 workspace_profile: WorkspaceProfile = Depends(
                     get_workspace_profile)
                 ) -> None:
        self.session = session
        self.workspace_profile = workspace_profile

        self.player_repository = PlayerRepository(session)
        self.role_repository = RoleRepository(session)

    async def find_player(self, player_id: int) -> Player:
        player = await self.player_repository.get_by_id(player_id)
        if player is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
        if player.creator.workspace_id != self.workspace_profile.workspace_id:
            raise HTTPException(HTTP_404_NOT_FOUND, "Not found")
        return player

    async def check_can_edit_player(self, player: Player):
        can_other = await self.role_repository.check_permission(self.workspace_profile.role, Permissions.change_player.value)
        can_self = (await self.role_repository.check_permission(self.workspace_profile.role, Permissions.change_your_player.value) and player.creator_id == self.workspace_profile.id)
        if not (can_other or can_self):
            raise HTTPException(HTTP_403_FORBIDDEN,
                                "Not enough permissions")

    async def check_can_set_roles(self, player: Player):
        can = await self.role_repository.check_permission(self.workspace_profile.role, Permissions.change_player_roles.value)
        if not can:
            raise HTTPException(HTTP_403_FORBIDDEN,
                                "Not enough permissions")

    @get("/{search_string}", response_model=list[PlayerBaseScheme])
    async def get_players_filtered(self, search_string: str):
        return await self.player_repository.get_by_workspace(self.workspace_profile.workspace, filter=f"%{search_string}%")

    @get("/", response_model=list[PlayerBaseScheme])
    async def get_players(self):
        return await self.player_repository.get_by_workspace(self.workspace_profile.workspace)

    @post("/", response_model=PlayerScheme)
    async def create_player(self,
                            request: CreatePlayerRequest):
        player = await self.player_repository.create(self.workspace_profile, request.username)
        if player is None:
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR, "Internal error")
        await self.session.commit()
        return player

    @patch("/{player_id}")
    async def patch_player(self,
                           player_id: int,
                           request: PatchPlayerRequest):
        player = await self.find_player(player_id)

        if request.username is not None:
            await self.check_can_edit_player(player)
            await self.player_repository.update_username(player, request.username)

        if request.is_flex is not None:
            await self.check_can_set_roles(player)
            await self.player_repository.update_flex(player, self.workspace_profile, request.is_flex)

        if request.roles is not None:
            await self.check_can_set_roles(player)
            await self.player_repository.update_roles(player, self.workspace_profile, request.roles)

        await self.session.commit()
        return {"message": "OK"}

    @delete("/{player_id}")
    async def delete_player(self,
                            player_id: int):
        player = await self.find_player(player_id)
        await self.check_can_edit_player(player)
        await self.player_repository.delete(player)
        await self.session.commit()
        return {"message": "OK"}
