from datetime import datetime


from fastapi import HTTPException
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import true
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from starlette import status
from starlette.status import HTTP_403_FORBIDDEN

from db.models.users import association_table
from schemas.token import Status
from schemas.user import UserOut
from schemas.job import JobCreate, JobOut, JobUpdate, JobDetail
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
        print(instance.user_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There is no object"
            )
        return instance

    async def create(
        self, obj_in: JobCreate, user_db: UserOut, db: AsyncSession
    ) -> JobOut:
        obj_dict = obj_in.dict()
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
            status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    async def get_all(self, db: AsyncSession, job_categories):
        query = select(self.model).filter(self.model.is_active == true()).order_by(self.model.created_at.desc())
        if job_categories is not None:
            query = (select(self.model)
                     .filter(self.model.category.in_([*job_categories]),
                             self.model.is_active == true()).order_by(self.model.created_at.desc()))
        instance = await paginate(db, query)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects"
            )
        return instance

    async def apply_to_vacancy(self, job_pk: int, user_db: UserOut, db: AsyncSession):
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
        return Status(message=True)

    async def delete(self, pk: int, db: AsyncSession, user_db: UserOut):
        job = await self.get_one(pk, db)
        if job.user_id == user_db.id or user_db.is_superuser:
            query = update(self.model).where(self.model.id == pk).values(is_active=False)
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
            status_code=HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )

    async def get_vacancy_appliers(
        self,
        job_pk: int,
        user_db: UserOut,
        db: AsyncSession,
    ):
        query = (
            select(self.model)
            .where(self.model.id == job_pk)
            .options(joinedload(Job.appliers))
        )
        db_obj = await db.execute(query)
        instance = db_obj.scalar()
        return instance


def get_jobs_service() -> JobsService:
    return JobsService()
