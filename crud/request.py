from database.models import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.request import RequestCreate


async def create_request(session: AsyncSession, request: RequestCreate):
    request = Request(**request.model_dump())
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


async def get_request(session: AsyncSession, request_id: int):
    stmt = select(Request).filter(Request.id == request_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def update_price(session: AsyncSession, request_id: int, price: int):
    stmt = (
        select(Request)
        .filter(Request.id == request_id)
        .with_for_update()
        .execution_options(sync_execution=True)
    )
    result = await session.execute(stmt)
    request = result.scalar_one_or_none()
    request.price = price
    await session.commit()
    await session.refresh(request)
    return request