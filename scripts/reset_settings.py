from DataBase.database import sessionmanager
from DataBase.repository import ProfileRepository
from DataBase.models import DEFAULT_PROFILE_DATA


async def reset_settings():
    async with sessionmanager.session() as session:
        profile_repository = ProfileRepository(session)
        id = int(input("Enter user id: "))
        profile = await profile_repository.get_by_id(id)
        if profile is None:
            print("Profile not found")
            return
        y = (input(f"Profile name: {profile.username}, continue? "))
        if "y" == y:
            profile.settings = DEFAULT_PROFILE_DATA
            await session.flush()
            await session.commit()

