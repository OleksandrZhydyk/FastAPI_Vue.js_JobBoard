from fastapi import HTTPException
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from src.db.base import db
from src.schemas.user import UserOut
from src.db.repositories.base import BaseService
from src.schemas.job import JobCreate, JobOut
from src.db.models.jobs import Job


class JobsService(BaseService[JobCreate, JobOut]):
    def __init__(self):
        super().__init__(Job)

    async def create(self, obj: JobCreate, user: UserOut) -> JobOut:
        obj_dict = obj.dict()
        obj_dict['user_id'] = user.id
        instance = self.model(**obj_dict)
        db.add(instance)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already registered")
        return instance

    async def update(self, pk: int, obj: JobCreate, user: UserOut) -> JobOut:
        job = await self.get_one(pk)
        if job.user_id == user.id or user.is_superuser:
            return await super().update(pk, obj)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Unauthorized for this action")



def get_jobs_service() -> JobsService:
    return JobsService()
