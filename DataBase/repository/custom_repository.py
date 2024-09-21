from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CustomRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session