from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.db.base import Base
from src.db.base import db


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_company = Column(Boolean, default=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow())
    updated_at = Column(DateTime, index=True, default=datetime.utcnow())

    @classmethod
    async def create(cls, **kwargs):
        user = cls(**kwargs)
        db.add(user)
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise
        return user

