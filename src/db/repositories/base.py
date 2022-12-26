from fastapi import status
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import update, delete
from starlette.exceptions import HTTPException

from src.db.base import Base
from src.db.base import db
from sqlalchemy.future import select


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(self, obj: CreateSchemaType) -> ModelType:
        instance = self.model(**obj.dict())
        db.add(instance)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Incorrect value was entered")
        return instance

    async def get_all(self) -> List[ModelType]:
        query = select(self.model)
        db_obj: List[ModelType] = await db.execute(query)
        instances = db_obj.scalars().all()
        if not instances:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no objects")
        return instances

    async def get_one(self, pk: int) -> ModelType:
        query = select(self.model).where(self.model.id == pk)
        db_obj = await db.execute(query)
        instance = db_obj.scalar()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no object")
        return instance

    async def update(self, pk: int, obj: ModelType) -> ModelType:
        query = update(self.model).where(self.model.id == pk).values(**obj.dict()).execution_options(synchronize_session="fetch")
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Incorrect value was entered")
        return obj.dict()

    async def delete(self, pk: int):
        query = delete(self.model).where(self.model.id == pk)
        await db.execute(query)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no object to delete")
        return True

