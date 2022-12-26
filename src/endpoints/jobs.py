from typing import List, Optional

from fastapi import APIRouter, Depends

from src.db.repositories.jobs import JobsService, get_jobs_service
from src.schemas.job import JobCreate, JobOut

router_jobs = APIRouter()


@router_jobs.post("/", response_model=JobOut)
async def create_user(obj: JobCreate, job_service: JobsService = Depends(get_jobs_service)) -> JobOut:
    return await job_service.create(obj)


@router_jobs.get("/", response_model=List[JobOut])
async def get_users(job_service: JobsService = Depends(get_jobs_service),) -> Optional[List[JobOut]]:
    return await job_service.get_all()


@router_jobs.get("/{pk}", response_model=JobOut)
async def get_one(pk: int, job_service: JobsService = Depends(get_jobs_service)) -> Optional[JobOut]:
    return await job_service.get_one(pk)


@router_jobs.put("/{pk}", response_model=JobOut)
async def update_user(obj: JobOut, pk: int, job_service: JobsService = Depends(get_jobs_service)) -> JobOut:
    return await job_service.update(pk, obj)


@router_jobs.delete("/{pk}", response_model=bool)
async def delete_user(pk: int, job_service: JobsService = Depends(get_jobs_service)) -> bool:
    return await job_service.delete(pk)
