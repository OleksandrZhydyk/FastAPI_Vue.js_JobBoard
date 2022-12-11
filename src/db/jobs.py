import datetime

import sqlalchemy

from src.db.base import metadata

jobs = sqlalchemy.Table(
    "jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column("email", sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column("title", sqlalchemy.String,),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean),
    sqlalchemy.Column("salary_from", sqlalchemy.Integer),
    sqlalchemy.Column("salary_to", sqlalchemy.Integer),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow()),
)
