from fastapi import APIRouter

from .Players.players import PlayerController
from .Profile.auth import AuthController
from .Profile.invite import InviteController
from .Profile.profile import ProfileController
from .Profile.settings import SettingsController
from .Profile.workspace import WorkspaceController

router = APIRouter(
    prefix="/api",
)

router.include_router(ProfileController.create_router())
router.include_router(AuthController.create_router())
router.include_router(InviteController.create_router())
router.include_router(SettingsController.create_router())
router.include_router(WorkspaceController.create_router())
router.include_router(PlayerController.create_router())