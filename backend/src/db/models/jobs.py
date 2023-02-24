from datetime import datetime

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Text, DateTime, Enum
from sqlalchemy.orm import relationship

from db.base import Base
from db.models.users import association_table
from schemas.job import JobCategory


# class JobCategory(str, enum.Enum):
#     finance = 'Finance'
#     marketing = 'Marketing'
#     agro = 'Agriculture'
#     it = 'IT'
#     metallurgy = 'Metallurgy'
#     medicine = 'Medicine'
#     construction = 'Construction'
#     building = 'Building'
#     services = 'Services'
#     miscellaneous = 'Miscellaneous'

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    email = Column(String)
    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title = Column(String, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow)
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    category = Column(Enum(JobCategory), server_default='miscellaneous', nullable=False)

    appliers = relationship("User", secondary=association_table, back_populates="vacancies")

    user = relationship("User")




