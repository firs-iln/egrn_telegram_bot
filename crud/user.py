from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User
from schemas.user import UserCreate
from database.enums import UserRolesEnum
from typing import Optional


async def get_user(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    result = await session.execute(select(User).filter(User.username == username))
    user = result.scalars().first()
    return user


async def create_user(session: AsyncSession, user: UserCreate) -> User:
    if await get_user(session, user.id):
        raise ValueError('This user already exists')

    user = User(**user.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, new_data: UserCreate) -> User:
    user = await get_user(session, new_data.id)
    if not user:
        raise ValueError('This user does not exist')

    for key, value in new_data.model_dump().items():
        if value is not None and key != 'id' and key != 'role':
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user


async def update_user_role(session: AsyncSession, username: str, role: UserRolesEnum) -> User:
    await session.execute(update(User).where(User.username == username).values(role=role))
    await session.commit()
    return await get_user_by_username(session, username)


async def get_admins(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User).filter(User.role == UserRolesEnum.ADMIN))
    return list(result.scalars().all())


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.execute(select(User))
    return list(result.scalars().all())