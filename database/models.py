from sqlalchemy import Column, BigInteger, Integer, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum, ClientTypeEnum

Base = declarative_base()


class Request(Base, AsyncAttrs):
    __tablename__ = 'requests'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cadnum = Column(String, nullable=False)
    fio_is_provided = Column(Boolean, nullable=False, default=False)
    result_file_filename = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
