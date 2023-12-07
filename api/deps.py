from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from typing import AsyncGenerator


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
