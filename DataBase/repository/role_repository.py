
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.models import Perm, Role, RolePerm
from .permission_repository import PermissionRepository


class RoleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Role]:
        stmt = select(Role).where(Role.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == name).limit(1)
        return await self.session.scalar(stmt)

    async def get_all(self) -> list[Role]:
        stmt = select(Role)
        return list((await self.session.scalars(stmt)).all())

    async def create(self, name: str) -> Optional[Role]:
        role = Role(name=name)
        self.session.add(role)
        await self.session.flush()
        return await self.get_by_id(role.id)

    async def add_permission(self, role: Role, permission: Perm):
        role_perm = RolePerm(role_id=role.id, perm_id=permission.id)
        self.session.add(role_perm)
        await self.session.flush()

    async def get_permissions(self, role: Role) -> list[Perm]:
        stmt = select(RolePerm).where(RolePerm.role_id == role.id)
        role_perms = (await self.session.scalars(stmt)).all()
        perms = []
        for i in role_perms:
            perms.append(i.perm)
        return perms

    async def check_permission(self, role: Role, name: str) -> bool:
        permission_repository = PermissionRepository(self.session)
        perm = await permission_repository.get_by_name(name)
        if perm is None:
            return False
        stmt = select(RolePerm).where(RolePerm.role_id ==
                                      role.id, RolePerm.perm_id == perm.id).limit(1)
        result = await self.session.scalar(stmt)
        return result is not None
