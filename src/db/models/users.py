from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.db.base import Base
from src.db.base import db


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_company = Column(Boolean, default=False)
    updated_at = Column(String, default=datetime.utcnow().isoformat()[:-3] + 'Z')
    created_at = Column(String, default=datetime.utcnow().isoformat()[:-3] + 'Z')
    # updated_at = Column(DateTime, default=datetime.utcnow())
