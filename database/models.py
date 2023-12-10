from sqlalchemy import Column, BigInteger, Integer, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum, ClientTypeEnum

from enum import Enum as pyEnum

Base = declarative_base()


class Request(Base, AsyncAttrs):
    __tablename__ = 'requests'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cadnum = Column(String, nullable=False)
    order_id = Column(BigInteger, nullable=False)
    fio_is_provided = Column(Boolean, nullable=False, default=False)
    r1r7_filename = Column(String, nullable=True)
    registry_filename = Column(String, nullable=True)


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=True)
    last_name: Mapped[str] = Column(String, nullable=True)
    role: Mapped[UserRolesEnum] = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
