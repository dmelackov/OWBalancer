from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from backend.dependency import PlayerServiceDepends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import WorkspaceProfile
from database.models.player import Player
from database.schemes import PlayerBaseScheme, PlayerScheme, CustomScheme
from domain.services import PlayerService
from backend.utils import WorkspaceProfileDepends, get_workspace_profile


class CreatePlayerRequest(BaseModel):
    username: str


class PatchPlayerRequest(BaseModel):
    username: Optional[str] = None
    is_flex: Optional[bool] = None
    roles: Optional[Annotated[str, Query(
        pattern="^[TDH]?[TDH]?[TDH]?$")]] = None


router = APIRouter(
    prefix="/players",
    tags=["players"]
)


@router.get("/{search_string}", response_model=list[PlayerBaseScheme])
async def get_players_filtered(
    search_string: str,
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends,
) -> list[Player]:
    return await player_service.get_players(workspace_profile.workspace, filter=f"%{search_string}%")


@router.get("/", response_model=list[PlayerBaseScheme])
async def get_players(
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends,
):
    return await player_service.get_players(workspace_profile.workspace)


@router.post("/", response_model=PlayerScheme)
async def create_player(
    request: CreatePlayerRequest,
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends,
):
    player = await player_service.create(workspace_profile, request.username)
    return player


@router.get("/{player_id}/customs", response_model=list[CustomScheme])
async def get_player_customs(
    player_id: int,
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends
):
    # TODO: реализовать логику
    pass


@router.patch("/{player_id}")
async def patch_player(
    player_id: int,
    request: PatchPlayerRequest,
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends
):
    player = await player_service.get_by_id(player_id)

    if request.username is not None:
        await player_service.set_name(workspace_profile, player, request.username)
    if request.is_flex is not None:
        await player_service.set_flex(workspace_profile, player, request.is_flex)
    if request.roles is not None:
        await player_service.set_roles(workspace_profile, player, request.roles)
    return {"message": "OK"}


@router.delete("/{player_id}")
async def delete_player(
    player_id: int,
    player_service: PlayerServiceDepends,
    workspace_profile: WorkspaceProfileDepends,
):
    player = await player_service.get_by_id(player_id)
    await player_service.delete(workspace_profile, player)
    return {"message": "OK"}
