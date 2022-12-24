from datetime import datetime
from sqlalchemy import update
from starlette.exceptions import HTTPException

from src.core.security import hash_password
from src.db.base import db
from src.db.repositories.base import BaseService
from src.schemas.user import UserIn, UserCreate, UserOut, UserBase
from src.db.models.users import User


class UsersService(BaseService[UserOut, UserCreate]):
    def __init__(self):
        super().__init__(User)

    async def create(self, obj: UserCreate) -> UserIn:
        obj_dict = obj.dict()
        hashed_password = hash_password(obj_dict.get('password'))
        db_obj = self.model(
            email=obj_dict.get('email'),
            name=obj_dict.get('name'),
            is_company=obj_dict.get('is_company'),
            is_active=obj_dict.get('is_active'),
            hashed_password=hashed_password
        )
        db.add(db_obj)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=409, detail="This email is already registered")
        return db_obj

    async def update(self, pk: int, obj: UserIn) -> UserOut:
        obj_dict = obj.dict()

        obj_dict['updated_at'] = datetime.utcnow().isoformat()[:-3]+'Z'
        print(obj_dict)
        query = update(self.model).where(self.model.id == pk)\
            .values(**obj_dict)\
            .execution_options(synchronize_session="fetch")
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return obj_dict


def get_users_service() -> UsersService:
    return UsersService()




# import datetime
# from typing import List, Optional

# from schemas.user import UserCreate
# from db.models.users import User
# from .base import BaseRepository
#
#
# class UserRepository(BaseRepository):
#
#     async def create_user(user: UserCreate):
#         user = await User.create(**user.dict())
#         return user



    # async def get_user(id: str):
    #     user = await User.get(id)
    #     return user

    # async def get_all(self, limit: int = 100, skip: int = 0) -> List[User]:
    #     query = User.select().limit(limit).offset(skip)
    #     return await self.database.fetch_all(query=query)
    #
    # async def get_by_id(self, id: int) -> Optional[User]:
    #     query = User.select().where(User.c.id == id).first()
    #     user = await self.database.fetch_one(query=query)
    #     if user is None:
    #         return None
    #     return User.parse_obj(user)
    #
    # async def create(self, u: UserCreate) -> User:
    #     user = User(
    #         name=u.name,
    #         email=u.email,
    #         hashed_password=hash_password(u.password),
    #         is_company=u.is_company,
    #         created_at=datetime.datetime.utcnow(),
    #         updated_at=datetime.datetime.utcnow()
    #     )
    #     user_attr_dict = {**user.dict()}
    #     user_attr_dict.pop("id", None)
    #     query = User.insert().values(**user_attr_dict)
    #     user.id = await self.database.execute(query)
    #     return user
    #
    # async def update(self, id: int, u: UserCreate) -> User:
    #     user = User(
    #         name=u.name,
    #         email=u.email,
    #         hashed_password=hash_password(u.password),
    #         is_company=u.is_company,
    #         created_at=datetime.datetime.utcnow(),
    #         updated_at=datetime.datetime.utcnow()
    #     )
    #     user_attr_dict = {**user.dict()}
    #     user_attr_dict.pop("id", None)
    #     user_attr_dict.pop("created_at", None)
    #     query = users.update().where(users.c.id == id).values(**user_attr_dict)
    #     await self.database.execute(query)
    #     return user
    #
    # async def get_by_email(self, email: str) -> Optional[User]:
    #     query = users.select().where(users.c.email == id).first()
    #     user = await self.database.fetch_one(query=query)
    #     if user is None:
    #         return None
    #     return User.parse_obj(user)
