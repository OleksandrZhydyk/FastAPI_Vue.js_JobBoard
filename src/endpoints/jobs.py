from typing import List, Optional

from fastapi import APIRouter, Depends

from src.core.security import check_company_credentials
from src.schemas.user import UserOut
from src.db.repositories.jobs import JobsService, get_jobs_service
from src.schemas.job import JobCreate, JobOut

router_jobs = APIRouter()


@router_jobs.post("/", response_model=JobOut)
async def create_job(obj: JobCreate, job_service: JobsService = Depends(get_jobs_service),
                     user: UserOut = Depends(check_company_credentials), ) -> JobOut:
    return await job_service.create(obj, user)


@router_jobs.get("/", response_model=List[JobOut])
async def get_jobs(job_service: JobsService = Depends(get_jobs_service),) -> Optional[List[JobOut]]:
    return await job_service.get_all()


@router_jobs.get("/{pk}", response_model=JobOut)
async def get_job(pk: int, job_service: JobsService = Depends(get_jobs_service)) -> Optional[JobOut]:
    return await job_service.get_one(pk)


@router_jobs.put("/{pk}", response_model=JobOut)
async def update_job(obj: JobOut, pk: int, job_service: JobsService = Depends(get_jobs_service),
                     user: UserOut = Depends(check_company_credentials)) -> JobOut:
    return await job_service.update(pk, obj, user)


@router_jobs.delete("/{pk}", response_model=bool)
async def delete_job(pk: int, job_service: JobsService = Depends(get_jobs_service),
                     user: UserOut = Depends(check_company_credentials)) -> bool:
    return await job_service.delete(pk)
