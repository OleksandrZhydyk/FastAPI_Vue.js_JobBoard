from datetime import datetime
from typing import List

from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from db.models.users import association_table
from schemas.user import UserOut
from schemas.job import JobCreate, JobOut, JobDetail, JobUpdate
from db.models.jobs import Job


class JobsService:
    def __init__(self):
        self.model = Job

    async def get_one(self, pk: int, db: AsyncSession) -> JobDetail:
        query = (
            select(self.model).where(self.model.id == pk).options(joinedload(Job.user))
        )
        db_obj = await db.execute(query)
        instance = db_obj.scalar()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There is no object"
            )
        return instance

    async def create(
        self, obj_in: JobCreate, user_db: UserOut, db: AsyncSession, job_category
    ) -> JobOut:
        obj_dict = obj_in.dict()
        obj_dict["category"] = job_category
        obj_dict["user_id"] = user_db.id
        instance = self.model(**obj_dict)
        db.add(instance)
        try:
            await db.commit()
        except Exception as e:
            print(e)
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered",
            )
        return instance

    async def update(
        self,
        pk: int,
        obj_in: JobUpdate,
        user_db: UserOut,
        db: AsyncSession,
    ) -> JobOut:
        job = await self.get_one(pk, db)
        if job.user_id == user_db.id or user_db.is_superuser:
            obj_dict = obj_in.dict(exclude_none=True)
            obj_dict["updated_at"] = datetime.utcnow()
            query = (
                update(self.model)
                .where(self.model.id == pk)
                .values(**obj_dict)
                .returning(self.model)
            )
            instance = await db.execute(query)
            try:
                await db.commit()
            except Exception:
                await db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Incorrect value was entered",
                )
            return instance.scalar_one()
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized for this action"
        )

    async def get_all(self, db: AsyncSession, job_category) -> List[Job]:
        query = select(self.model)
        if job_category is not None:
            query = select(self.model).filter(self.model.category == job_category)
        db_obj = await paginate(db, query)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects"
            )
        return db_obj

    async def apply_to_job(self, job_pk: int, user_db: UserOut, db: AsyncSession):
        query = insert(association_table).values(
            {"user_id": user_db.id, "job_id": job_pk}
        )
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email is already registered",
            )
        return True

    async def delete(self, pk: int, db: AsyncSession):
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

    async def get_job_appliers(
        self,
        job_pk: int,
        user_db: UserOut,
        db: AsyncSession,
    ):
        users_query = (
            select(self.model)
            .where(self.model.id == job_pk)
            .options(joinedload(Job.appliers))
        )
        db_obj = await db.execute(users_query)
        instance = db_obj.scalar()
        return instance


def get_jobs_service() -> JobsService:
    return JobsService()
