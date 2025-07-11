from fastapi import APIRouter

# from .Players.players import router as PlayerController
from .Profile.auth import router as AuthController
from .Profile.invite import router as InviteController
from .Profile.profile import router as ProfileController
from .Profile.settings import router as SettingsController
from .Profile.workspace import router as WorkspaceController

router = APIRouter(
    prefix="/api",
)

router.include_router(ProfileController)
router.include_router(AuthController)
router.include_router(InviteController)
router.include_router(SettingsController)
router.include_router(WorkspaceController)
# router.include_router(PlayerController)
