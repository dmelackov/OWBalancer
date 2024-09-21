from typing import Annotated, Optional

from fastapi import Depends, Query
from fastapi_controllers import Controller, delete, get, patch, post
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models.workspace_profile import WorkspaceProfile
from DataBase.schemes.player import PlayerBaseScheme, PlayerScheme
from Site.service.player_service import PlayerService
from Site.utils import get_workspace_profile


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

        self.player_service = PlayerService(session)

    @get("/{search_string}", response_model=list[PlayerBaseScheme])
    async def get_players_filtered(self, search_string: str):
        return await self.player_service.get_players(self.workspace_profile.workspace, filter=f"%{search_string}%")

    @get("/", response_model=list[PlayerBaseScheme])
    async def get_players(self):
        return await self.player_service.get_players(self.workspace_profile.workspace)

    @post("/", response_model=PlayerScheme)
    async def create_player(self,
                            request: CreatePlayerRequest):
        player = await self.player_service.create(self.workspace_profile, request.username)
        await self.session.commit()
        return player

    @patch("/{player_id}")
    async def patch_player(self,
                           player_id: int,
                           request: PatchPlayerRequest):
        player = await self.player_service.get_by_id(player_id)

        if request.username is not None:
            await self.player_service.set_name(self.workspace_profile, player, request.username)
        if request.is_flex is not None:
            await self.player_service.set_flex(self.workspace_profile, player, request.is_flex)
        if request.roles is not None:
            await self.player_service.set_roles(self.workspace_profile, player, request.roles)

        await self.session.commit()
        return {"message": "OK"}

    @delete("/{player_id}")
    async def delete_player(self,
                            player_id: int):
        player = await self.player_service.get_by_id(player_id)
        await self.player_service.delete(self.workspace_profile, player)
        await self.session.commit()
        return {"message": "OK"}
