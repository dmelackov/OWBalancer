import json
from datetime import timedelta

from fastapi import Depends, HTTPException, Response
from fastapi_login.exceptions import InvalidCredentialsException
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST

from sqlalchemy.ext.asyncio import AsyncSession
from DataBase.database import get_db_session

from DataBase.models.profile import Profile
from DataBase.repository.profile_repository import ProfileRepository
from Site.loginManager import manager

from fastapi_controllers import Controller, post


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
        self.profile_repository = ProfileRepository(session)

    @post("/login")
    async def login(self, response: Response, request: LoginRequest):
        profile = await self.profile_repository.get_by_auth(request.username, request.password)
        if profile is None:
            raise InvalidCredentialsException
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
        if request.password != request.password_again:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Passwords don't match")
        if await self.profile_repository.get_by_username(request.username) is not None:
            raise HTTPException(HTTP_400_BAD_REQUEST, "User already exist")
        await self.profile_repository.registration(request.username, request.password)
        await self.session.commit()
        return {"message": "OK"}

    @post("/logout")
    def logout(self, response: Response, user: Profile = Depends(manager)):
        response.set_cookie("access-token", "", max_age=0, httponly=True)
        response.set_cookie("workspace", "", max_age=0)
        return {"message": "OK"}
