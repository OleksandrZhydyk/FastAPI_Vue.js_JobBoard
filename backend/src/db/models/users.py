from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from db.base import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("job_id", ForeignKey("jobs.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    is_company = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_jobs = relationship("Job", backref="company_created")
    avatar = Column(String)
    resume = Column(String)

    vacancies = relationship(
        "Job", secondary=association_table, back_populates="appliers", order_by="Job.created_at"
    )
