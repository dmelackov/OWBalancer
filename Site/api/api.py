from fastapi import APIRouter

from Site.api.Players.players import PlayerController
from Site.api.Profile.auth import AuthController
from Site.api.Profile.invite import InviteController
from Site.api.Profile.profile import ProfileController
from Site.api.Profile.settings import SettingsController
from Site.api.Profile.workspace import WorkspaceController

router = APIRouter(
    prefix="/api",
)

router.include_router(ProfileController.create_router())
router.include_router(AuthController.create_router())
router.include_router(InviteController.create_router())
router.include_router(SettingsController.create_router())
router.include_router(WorkspaceController.create_router())
router.include_router(PlayerController.create_router())