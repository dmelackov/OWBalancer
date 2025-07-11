from sqlalchemy.ext.asyncio import AsyncSession

from balancer_models.models import Player, Custom, WorkspaceProfile

from .player_service import PlayerService
from .workspace_profile_service import WorkspaceProfileService
from .workspace_service import WorkspaceService

class CustomService:
    def __init__(self, workspace_service: WorkspaceService, workspace_profile_service: WorkspaceProfileService) -> None:
        self.workspace_service = workspace_service
        self.workspace_profile_service = workspace_profile_service

    def get_by_player(self, player: Player) -> list[Custom]:
        ...

    def get_by_id(self, id: int) -> Custom:
        ...

    def get_by_bind(self, player: Player, workspace_profile: WorkspaceProfile) -> Custom:
        ...

    def is_your_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool:
        ...

    def can_edit_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool:
        ...

    def check_edit_custom(self, initiator: WorkspaceProfile, target: Custom):
        ...

    def can_delete_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool:
        ...

    def check_delete_custom(self, initiator: WorkspaceProfile, target: Custom):
        ...

    def set_rating(self, tank_rating: int | None = None,
                    damage_rating: int | None = None, 
                    support_rating: int | None = None):
        ...

    def delete(self, initiator: WorkspaceProfile, custom: Custom):
        ...