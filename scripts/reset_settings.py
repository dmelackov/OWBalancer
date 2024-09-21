from DataBase.database import sessionmanager
from DataBase.repository.permission_repository import PermissionRepository
from DataBase.repository.role_repository import RoleRepository
from DataBase.repository.profile_repository import ProfileRepository
from DataBase.models.profile import DEFAULT_PROFILE_DATA


async def reset_settings():
    async with sessionmanager.session() as session:
        profile_repository = ProfileRepository(session)
        id = int(input("Enter user id: "))
        profile = await profile_repository.get_by_id(id)
        y = (input(f"Profile name: {profile.username}, continue? "))
        if "y" == y:
            profile.settings = DEFAULT_PROFILE_DATA
            await session.flush()
            await session.commit()

