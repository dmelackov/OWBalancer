from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependency import ProfileServiceDepends
from balancer_models.models import Profile
from domain.schemes import Settings
from domain.services import ProfileService
from backend.utils import ProfileDepends, get_ok_response

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)


@router.get(
    "/default",
    response_model=Settings,
    summary="Get default settings"
)
async def get_default_settings(
    profile_service: ProfileServiceDepends
):
    """
    Get default settings

    Default settings are the same for all profiles.
    They are used as a starting point for a new profile.
    """
    return profile_service.get_default_settings()


@router.get(
    "/",
    response_model=Settings,
    summary="Get profile settings"
)
async def get_profile_settings(
    profile_service: ProfileServiceDepends,
    profile: ProfileDepends,
):
    """
    Get profile settings

    Return the settings of the current profile.
    """
    return profile_service.get_settings(profile)


@router.post(
    "/",
    summary="Set profile settings",
    responses=get_ok_response("Settings updated")
)
async def set_profile_settings(
    settings: Settings,
    profile_service: ProfileServiceDepends,
    profile: ProfileDepends,
):
    """
    Set profile settings

    Replace the current settings of the profile with the given ones.
    """
    await profile_service.set_settings(profile, settings)
    return {"message": "OK"}