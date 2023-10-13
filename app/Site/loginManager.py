from fastapi_login import LoginManager
import json

from app.params import SECRET_KEY
from app.DataBase.db import Profile
from app.Site.exceptions import NotAuthenticatedException

manager = LoginManager(SECRET_KEY, token_url='/api/auth/login',
                       use_cookie=True, custom_exception=NotAuthenticatedException)


@manager.user_loader()
def load_user(userStr: str):  # could also be an asynchronous function
    user: dict = json.loads(userStr)
    id = user.get("ID", None)
    secret = user.get("Secret", None)
    if id is None or user is None:
        return None
    user = Profile.select().where(Profile.ID == id, Profile.Secret == secret)
    if user:
        return user[0]
    else:
        return None
