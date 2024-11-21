from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import Player, Custom, WorkspaceProfile

from .player_service import PlayerService
from .workspace_profile_service import WorkspaceProfileService
from .workspace_service import WorkspaceService

class CustomService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.workspace_service = WorkspaceService(session)
        self.workspace_profile_service = WorkspaceProfileService(session)

    def get_by_player(self, player: Player) -> list[Custom]:
        pass

    def get_by_id(self, id: int) -> Custom:
        pass

    def get_by_bind(self, player: Player, workspace_profile: WorkspaceProfile) -> Custom:
        pass

    def is_your_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool:
        pass

    def can_edit_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool:
        pass

    def check_edit_custom(self, initiator: WorkspaceProfile, target: Custom):
        pass

    def can_delete_custom(self, initiator: WorkspaceProfile, target: Custom) -> bool
        pass

    def check_delete_custom(self, initiator: WorkspaceProfile, target: Custom):
        pass

    def set_rating(self, tank_rating: int | None = None,
                    damage_rating: int | None = None, 
                    support_rating: int | None = None):
        pass

    def delete(self, initiator: WorkspaceProfile, custom: Custom):
        pass