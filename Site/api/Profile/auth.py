import json
from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from fastapi_controllers import Controller, post
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.database import get_db_session
from DataBase.models import Profile
from Site.exception_mapping import exception_mapping, generate_responses_for_endpoint
from domain.exceptions.profile_exceptions import InvalidCredentialsException, PasswordDontMatchException, ProfileAlreadyExists
from domain.services import ProfileService
from Site.loginManager import manager
from Site.utils import get_ok_response


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

    @post("/login",
          summary="Login user in system",
          responses={
              **get_ok_response("Login successful"),
              **generate_responses_for_endpoint(
                  allowed_exceptions=[
                      InvalidCredentialsException
                  ],
              )
          })
    async def login(self, response: Response, request: LoginRequest):
        """
        Login user and return access token.

        Args:
        - response (Response): Response object to set cookie.
        - request (LoginRequest): Request with username, password and remember_me flag.

        Returns:
        - dict: Dict with message "OK".
        """
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

    @post("/registration",
          summary="Register a new user",
          responses={
              **get_ok_response("Register successful"),
              **generate_responses_for_endpoint(
                  allowed_exceptions=[
                      PasswordDontMatchException,
                      ProfileAlreadyExists
                  ],
              )
          })
    async def registration(self, request: RegistrationRequest):
        """
        Register a new user.

        Args:
        - request (RegistrationRequest): Request containing username, password, and password confirmation.

        Returns:
        - dict: Dict with message "OK" upon successful registration.
        """
        await self.profile_service.registration(request.username, request.password, request.password_again)
        await self.session.commit()
        return {"message": "OK"}

    @post("/logout",
          summary="Logout the user",
          responses={
              **get_ok_response("Logout successful"),
          })
    def logout(self, response: Response, profile: Profile = Depends(manager)):
        """
        Logout the user and clear workspace.

        Args:
        - response (Response): Response object to clear cookies.
        - profile (Profile): Profile of the user to logout.

        Returns:
        - dict: Dict with message "OK" upon successful logout.
        """
        response.set_cookie("access-token", "", max_age=0, httponly=True)
        response.set_cookie("workspace", "", max_age=0)
        return {"message": "OK"}
