from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
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
        db_obj = self.model(**obj.dict())
        db.add(db_obj)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return db_obj

    async def get_all(self) -> List[ModelType]:
        query = select(self.model)
        db_obj: List[ModelType] = await db.execute(query)
        db_obj = db_obj.scalars().all()
        if not db_obj:
            raise HTTPException(status_code=404, detail="There are no users")
        return db_obj
