from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from database.enums import UserRolesEnum


class UserBase(BaseModel):
    id: Optional[int]
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRolesEnum = UserRolesEnum.USER


class UserCreate(UserBase):
    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRolesEnum = UserRolesEnum.USER


class UserResponse(UserBase):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)

    id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRolesEnum

    created_at: datetime
