from typing import Optional, List
from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import check_company_credentials, get_current_active_user
from db.base import get_session
from db.repositories.jobs import JobsService, get_jobs_service
from schemas.custom_page import Page
from schemas.job import JobCreate, JobOut, JobApplied, JobUpdate, JobCategory, JobDetail
from schemas.token import Status
from schemas.user import UserOut, UserInDB

router_vacancies = APIRouter()


@router_vacancies.post("/", response_model=JobOut)
async def create_job(
    obj_in: JobCreate,
    job_service: JobsService = Depends(get_jobs_service),
    current_user: UserOut = Depends(check_company_credentials),
    db: AsyncSession = Depends(get_session),
):
    return await job_service.create(obj_in, current_user, db)


@router_vacancies.get("/", response_model=Page[JobOut])
async def get_vacancies(
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
    job_categories: List[JobCategory] = Query(None)
):
    return await job_service.get_all(db, job_categories)


@router_vacancies.get("/me", response_model=List[JobOut])
async def get_company_jobs(
    job_service: JobsService = Depends(get_jobs_service),
    current_user: UserInDB = Depends(check_company_credentials),
    db: AsyncSession = Depends(get_session),
):
    return await job_service.get_company_vacancies(current_user, db)


@router_vacancies.get("/{pk}", response_model=JobDetail)
async def get_job(
    pk: int,
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
) -> Optional[JobDetail]:
    return await job_service.get_one(pk, db)


@router_vacancies.put("/{pk}", response_model=JobOut)
async def update_job(
    obj: JobUpdate,
    pk: int,
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(check_company_credentials),
):
    return await job_service.update(pk, obj, current_user, db)


@router_vacancies.post("/{pk}/apply", response_model=Status)
async def apply_to_job(
    pk: int,
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(get_current_active_user),
):
    return await job_service.apply_to_vacancy(pk, current_user, db)


@router_vacancies.get("/{pk}/apply", response_model=JobApplied)
async def vacancy_appliers(
    pk: int,
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(check_company_credentials),
):
    return await job_service.get_vacancy_appliers(pk, current_user, db)


@router_vacancies.delete("/{pk}", response_model=Status)
async def delete_job(
    pk: int,
    job_service: JobsService = Depends(get_jobs_service),
    db: AsyncSession = Depends(get_session),
    current_user: UserOut = Depends(check_company_credentials),
) -> Status:
    return await job_service.delete(pk, db, current_user)
