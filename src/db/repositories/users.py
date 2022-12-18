import datetime
from typing import List, Optional

from src.core.security import hash_password
from db.models.users import users
from models import User, UserCreate
from .base import BaseRepository


class UserRepository(BaseRepository):

    async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
        query = users.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[User]:
        query = users.select().where(users.c.id == id).first()
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)

    async def create(self, u: UserCreate) -> User:
        user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        user_attr_dict = {**user.dict()}
        user_attr_dict.pop("id", None)
        query = users.insert().values(**user_attr_dict)
        user.id = await self.database.execute(query)
        return user

    async def update(self, id: int, u: UserCreate) -> User:
        user = User(
            name=u.name,
            email=u.email,
            hashed_password=hash_password(u.password),
            is_company=u.is_company,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        user_attr_dict = {**user.dict()}
        user_attr_dict.pop("id", None)
        user_attr_dict.pop("created_at", None)
        query = users.update().where(users.c.id == id).values(**user_attr_dict)
        await self.database.execute(query)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        query = users.select().where(users.c.email == id).first()
        user = await self.database.fetch_one(query=query)
        if user is None:
            return None
        return User.parse_obj(user)
