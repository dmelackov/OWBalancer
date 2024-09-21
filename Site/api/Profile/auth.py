import json
from datetime import timedelta

from fastapi import Depends, Response
from fastapi_controllers import Controller, post
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models.profile import Profile
from Site.loginManager import manager
from Site.service.profile_service import ProfileService


class LoginRequest(BaseModel):
    username: str
    password: str
    remember_me: bool


class RegistrationRequest(BaseModel):
    username: str
    password: str
    password_again: str


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.profile_service = ProfileService(session)

    @post("/login")
    async def login(self, response: Response, request: LoginRequest):
        profile = await self.profile_service.login(request.username, request.password)

        user = {"ID": profile.id, "Secret": profile.secret}
        access_token = manager.create_access_token(
            data=dict(sub=json.dumps(user)),
            expires=timedelta(
                days=30) if request.remember_me else timedelta(days=1)
        )
        response.set_cookie("access-token", access_token, max_age=60 *
                            60*24*30 if request.remember_me else 60*60*24, httponly=True)
        return {"message": "OK"}

    @post("/registration")
    async def registration(self, request: RegistrationRequest):
        await self.profile_service.registration(request.username, request.password, request.password_again)
        await self.session.commit()
        return {"message": "OK"}

    @post("/logout")
    def logout(self, response: Response, profile: Profile = Depends(manager)):
        response.set_cookie("access-token", "", max_age=0, httponly=True)
        response.set_cookie("workspace", "", max_age=0)
        return {"message": "OK"}
