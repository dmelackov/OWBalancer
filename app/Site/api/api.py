from fastapi import APIRouter
import app.Site.api.Profile.auth as Auth
import app.Site.api.Profile.profile as Profile
import app.Site.api.Profile.workspace as Workspace
import app.Site.api.Profile.settings as Settings
import app.Site.api.Players.players as Players
import app.Site.api.Players.customs as Customs
import app.Site.api.Lobby.lobby as Lobby
import app.Site.api.Lobby.balance as Balance
router = APIRouter(
    prefix="/api",
)

router.include_router(Profile.router)
router.include_router(Auth.router)
router.include_router(Workspace.router)
router.include_router(Settings.router)
router.include_router(Players.router)
router.include_router(Customs.router)
router.include_router(Lobby.router)
router.include_router(Balance.router)