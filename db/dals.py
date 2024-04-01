from typing import Optional
from sqlalchemy import and_, delete, update, select
from db.models import Role, Service, User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound


class UserDAL:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, email: str, hashed_password: str) -> User:
        username = email.split("@")[0]
        user = User(username=username, email=email, password=hashed_password)
        self.db.add(user)
        await self.db.flush()

        await self.add_user_role(
            user_id=user.id, role=Role.CLIENT, service=Service.AUTH
        )
        return user

    async def delete_user(self, email: str) -> None:
        query = delete(User).where(User.email == email)
        await self.db.execute(query)

    async def get_user(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.fetchone()
        return user[0] if user else None

    async def get_all_users(self, offset: int, limit: int) -> list[User | None]:
        query = select(User).offset(offset).limit(limit)
        users = await self.db.execute(query)
        return list(users.scalars())

    async def add_user_role(self, user_id: str, role: str, service: str) -> UserRole:
        role = UserRole(user_id=user_id, role=role, service=service)
        self.db.add(role)
        await self.db.flush()
        return role

    async def update_user_role(self, user_id: str, role: str, service: str) -> None:
        query = (
            update(UserRole)
            .where(and_(UserRole.user_id == user_id, UserRole.service == service))
            .values(role=role)
            .returning(UserRole)
        )
        result = await self.db.execute(query)
        updated_role = result.fetchone()
        return updated_role[0]

    async def check_service_for_user_is_exists(self, user_id, service) -> bool:
        query = select(UserRole).where(
            and_(UserRole.user_id == user_id, UserRole.service == service)
        )
        result = await self.db.execute(query)
        role = result.first()
        return bool(role)

    async def is_admin(self, user_id) -> bool:
        query = select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.service == Service.AUTH,
            UserRole.role == Role.ADMIN,
        )
        result = await self.db.execute(query)
        is_admin = result.first()
        return bool(is_admin)
