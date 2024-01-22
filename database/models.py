from sqlalchemy import Column, BigInteger, Integer, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import declarative_base, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs

from datetime import datetime

from .enums import UserRolesEnum, RequestStatusEnum

Base = declarative_base()


class Request(Base, AsyncAttrs):
    __tablename__ = 'requests'

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    cadnum = Column(String, nullable=False)
    order_id = Column(BigInteger, nullable=False)

    fio_is_provided = Column(Boolean, nullable=False, default=False)

    extract_filename = Column(String, nullable=True)
    r1r7_filename = Column(String, nullable=True)
    registry_filename = Column(String, nullable=True)

    total_area = Column(Integer, nullable=True)

    room_rows_count = Column(Integer, nullable=True)
    fio_rows_count = Column(Integer, default=0, nullable=True)

    reestr_api_order_id = Column(String, nullable=True)

    status = Column(Enum(RequestStatusEnum), default=RequestStatusEnum.CREATED)


class User(AsyncAttrs, Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    username: Mapped[str] = Column(String, unique=True, nullable=True)
    first_name: Mapped[str] = Column(String, nullable=True)
    last_name: Mapped[str] = Column(String, nullable=True)
    role: Mapped[UserRolesEnum] = Column(Enum(UserRolesEnum), default=UserRolesEnum.USER)

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
