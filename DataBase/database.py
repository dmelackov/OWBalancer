import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from DataBase.models import Base
from Static.params import (DB_HOST, DB_NAME, DB_PORT, DB_TYPE, DB_USER_LOGIN,
                           DB_USER_PASSWORD)

connect_string = ""


if DB_TYPE == "mysql":
    connect_string = f"mysql+pymysql: //{DB_USER_LOGIN}: {
        DB_USER_PASSWORD}@{DB_HOST}: {DB_PORT}/{DB_NAME}"
else:
    connect_string = f"sqlite+aiosqlite: ///./{DB_NAME}2.db"


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(connect_string, {"echo": False})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


async def create_db_and_tables():
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
