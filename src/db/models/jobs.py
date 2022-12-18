import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, Text

from src.db.base import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    email = Column(String)
    user_id = Column(ForeignKey('users.id'), nullable=True)
    title = Column(String, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default="False")
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
