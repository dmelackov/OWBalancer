import json
from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependency import ProfileServiceDepends
from balancer_models.models import Profile
from backend.exception_mapping import exception_mapping, generate_responses_for_endpoint
from domain.exceptions.profile_exceptions import InvalidCredentialsException, PasswordDontMatchException, ProfileAlreadyExists
from domain.services import ProfileService
from backend.utils import ProfileDepends, get_ok_response


class LoginRequest(BaseModel):
    username: str
    password: str


class RegistrationRequest(BaseModel):
    username: str
    password: str
    password_again: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/login",
    summary="Login user in system",
    responses={
        **get_ok_response("Login successful"),
        **generate_responses_for_endpoint(
            allowed_exceptions=[InvalidCredentialsException]
        )
    }
)
async def login(
    response: Response,
    request: LoginRequest,
    profile_service: ProfileServiceDepends
):
    profile = await profile_service.login(request.username, request.password)

    user_data = {"ID": profile.id, "Secret": profile.secret}
    access_token = manager.create_access_token(
        data={"sub": json.dumps(user_data)},
        expires=timedelta(days=30)
    )
    response.set_cookie("access-token", access_token,
                        max_age=60 * 60 * 24 * 30, httponly=True)
    return {"message": "OK"}


@router.post(
    "/registration",
    summary="Register a new user",
    responses={
        **get_ok_response("Register successful"),
        **generate_responses_for_endpoint(
            allowed_exceptions=[
                PasswordDontMatchException, ProfileAlreadyExists]
        )
    }
)
async def registration(
    request: RegistrationRequest,
    profile_service: ProfileServiceDepends
):
    await profile_service.registration(request.username, request.password, request.password_again)
    return {"message": "OK"}


@router.post(
    "/logout",
    summary="Logout the user",
    responses={
        **get_ok_response("Logout successful"),
    }
)
def logout(
    response: Response,
    profile: ProfileDepends
):
    response.set_cookie("access-token", "", max_age=0, httponly=True)
    response.set_cookie("workspace", "", max_age=0)
    return {"message": "OK"}
