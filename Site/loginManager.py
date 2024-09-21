import json

from fastapi_login import LoginManager

from DataBase.database import sessionmanager
from DataBase.repository.profile_repository import ProfileRepository
from Site.exceptions import NotAuthenticatedException
from Static.params import SECRET_KEY

manager = LoginManager(SECRET_KEY, token_url='/api/auth/login',
                       use_cookie=True, custom_exception=NotAuthenticatedException)


@manager.user_loader()
async def load_user(userStr: str):  # could also be an asynchronous function
    async with sessionmanager.session() as session:
        profileRepository = ProfileRepository(session)
        user: dict = json.loads(userStr)
        id = user.get("ID", None)
        secret = user.get("Secret", None)
        if id is None or user is None:
            return None
        profile = await profileRepository.get_by_id(id)
        if profile is None:
            return None
        if profile.secret == secret:
            return profile
        return None
