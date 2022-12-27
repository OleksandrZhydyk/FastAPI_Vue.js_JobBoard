from src.db.repositories.base import BaseService
from src.schemas.job import JobCreate, JobOut
from src.db.models.jobs import Job


class JobsService(BaseService[JobCreate, JobOut]):
    def __init__(self):
        super().__init__(Job)


def get_jobs_service() -> JobsService:
    return JobsService()
