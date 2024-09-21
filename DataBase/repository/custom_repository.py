from sqlalchemy.ext.asyncio import AsyncSession


class CustomRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
