from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND)

from DataBase.permissions import Permissions

router = APIRouter(
    prefix="/custom",
    tags=["custom"]
)


"""
patch - /{custom_id}  
    only sr
post - /
delete - /{custom_id}

edit need: 
Permissions.change_your_custom
Permissions.delete_your_custom or Permissions.delete_custom
Permissions.create_custom

services:
CustomService
WorkspaceProfileService
"""
