from datetime import datetime
from typing import List

from fastapi import status
from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from core.iofiles import upload_file
from core.security import hash_password
from schemas.token import Status
from schemas.user import UserCreate, UserOut
from db.models.users import User


class UsersService:
    def __init__(self):
        self.model = User

    async def create(self, obj_in: UserCreate, db: AsyncSession) -> UserOut:
        obj_dict = obj_in.dict()
        hashed_password = hash_password(obj_dict.get("password"))
        db_obj = self.model(
            email=obj_dict.get("email"),
            is_company=obj_dict.get("is_company"),
            is_active=True,
            hashed_password=hashed_password,
        )
        db.add(db_obj)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered",
            )
        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database error: {err}",
            )
        return db_obj

    async def update(
        self, user_update_data, avatar, clear_avatar, resume, clear_resume, user_db: UserOut, db: AsyncSession
    ) -> UserOut:
        obj_dict = user_update_data.dict(exclude_none=True)
        if avatar and not clear_avatar:
            path_avatar = await upload_file('avatars', avatar)
            obj_dict["avatar"] = path_avatar
        if clear_avatar:
            obj_dict["avatar"] = None
        if resume and not clear_resume:
            path_resume = await upload_file('resumes', resume)
            obj_dict["resume"] = path_resume
        if clear_resume:
            obj_dict["resume"] = None
        if obj_dict.get("password"):
            hashed_password = hash_password(obj_dict["password"])
            del obj_dict["password"]
            obj_dict["hashed_password"] = hashed_password
        obj_dict["updated_at"] = datetime.utcnow()
        query = (
            update(self.model)
            .where(self.model.id == user_db.id)
            .values(**obj_dict)
            .returning(self.model)
        )
        try:
            db_obj = await db.execute(query)
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered",
            )
        except Exception as err:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Database error: {err}",
            )
        # a = db_obj.scalar()
        # a = db_obj.scalar_one()
        a = db_obj.one()

        print(a)
        # return a
        return a[0]

    async def get_all(self, db: AsyncSession) -> List[UserOut]:
        query = select(self.model)
        db_obj = await paginate(db, query)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects"
            )
        return db_obj

    async def get_one(self, pk: int, user_db: UserOut, db: AsyncSession) -> UserOut:
        if user_db.is_company or user_db.is_superuser or user_db.id == pk:
            query = select(self.model).where(self.model.id == pk).options(joinedload(User.vacancies))
            db_obj = await db.execute(query)
            instance = db_obj.scalar()
            if not instance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="There is no object"
                )
            return instance
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    async def delete(self, pk: int, user_db: UserOut, db: AsyncSession,) -> Status:
        user = await self.get_one(pk, user_db, db)
        if user.id == user_db.id or user_db.is_superuser:
            query = delete(self.model).where(self.model.id == pk)
            await db.execute(query)
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="There is no object to delete",
                )
            return Status(message=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )


def get_users_service() -> UsersService:
    return UsersService()
