from datetime import datetime
from typing import List

from fastapi import status
from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.security import hash_password
from db.models.jobs import Job
from schemas.user import UserCreate, UserOut, UserUpdate
from db.models.users import User


class UsersService:
    def __init__(self):
        self.model = User

    async def create(self, obj_in: UserCreate, db: AsyncSession) -> UserOut:
        obj_dict = obj_in.dict()
        hashed_password = hash_password(obj_dict.get("password"))
        db_obj = self.model(
            email=obj_dict.get("email"),
            name=obj_dict.get("name"),
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
        self, obj_in: UserUpdate, user_db: UserOut, db: AsyncSession
    ) -> UserOut:
        obj_dict = obj_in.dict(exclude_none=True)
        obj_dict["updated_at"] = datetime.utcnow()
        if obj_dict.get("password"):
            hashed_password = hash_password(obj_dict["password"])
            del obj_dict["password"]
            obj_dict["hashed_password"] = hashed_password
        query = (
            update(self.model)
            .where(self.model.id == user_db.id)
            .values(**obj_dict)
            .returning(self.model)
        )
        instance = await db.execute(query)
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
        return instance.scalar()

    async def get_all(self, db: AsyncSession) -> List[UserOut]:
        query = select(self.model)
        db_obj = await paginate(db, query)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects"
            )
        return db_obj

    async def get_company_jobs(self, user_db: UserOut, db: AsyncSession):
        query = select(Job).filter(user_db.id == Job.user_id)
        db_obj = await db.execute(query)
        instance = db_obj.scalars().all()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects"
            )
        return instance

    async def get_one(self, pk: int, db: AsyncSession) -> UserOut:
        query = select(self.model).where(self.model.id == pk)
        db_obj = await db.execute(query)
        instance = db_obj.scalar()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There is no object"
            )
        return instance

    async def delete(self, pk: int, db: AsyncSession) -> bool:
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
        return True


def get_users_service() -> UsersService:
    return UsersService()
