from datetime import datetime
from importlib.metadata import metadata

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permission', JSON),
)


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey("roles.id")),
)