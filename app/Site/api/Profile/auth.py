from fastapi import APIRouter, Form, Response, HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
from typing_extensions import Annotated
from fastapi_login.exceptions import InvalidCredentialsException
from datetime import timedelta
import json

from app.DataBase.db import Profile
from app.Site.loginManager import manager

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()], remember_me: Annotated[bool, Form()],):
    profile = Profile.check(username, password).data
    if not profile:
        raise InvalidCredentialsException

    user = {"ID": profile.ID, "Secret": profile.Secret}

    access_token = manager.create_access_token(
        data=dict(sub=json.dumps(user)),
        expires=timedelta(days=30) if remember_me else None
    )
    response.set_cookie("access-token", access_token, max_age=60 *
                        60*24*30 if remember_me else None, httponly=True)
    return {"message": "OK"}


@router.post("/registration")
def registration(username: Annotated[str, Form()], password: Annotated[str, Form()], password_again: Annotated[str, Form()]):
    if password != password_again:
        raise HTTPException(HTTP_400_BAD_REQUEST, "Passwords don't match")
    if Profile.getProfile(username):
        raise HTTPException(HTTP_400_BAD_REQUEST, "User already exist")
    Profile.create(username, password)
    return {"message": "OK"}


@router.post("/logout")
def logout(response: Response, user: Profile = Depends(manager)):
    response.set_cookie("access-token", "", max_age=0, httponly=True)
    response.set_cookie("workspace", "", max_age=0)
    return {"message": "OK"}
