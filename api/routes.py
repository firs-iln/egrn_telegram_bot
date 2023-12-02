from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from api.deps import get_session

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from crud import request as request_service
from schemas.request import RequestCreate, RequestResponse

from bot import telegram_app
from sqlalchemy.ext.asyncio import AsyncSession
import io

from .types import OrderCallbackInput

from client_server_api import client_server_api

root_router = APIRouter(
    prefix="/api/v1",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@root_router.post("/request/")
async def create_request(
    cadnum: str,
    fio_is_provided: bool,
    session: AsyncSession = Depends(get_session),
) -> RequestResponse:
    request = await request_service.create_request(
        session, RequestCreate(cadnum=cadnum)
    )

    return RequestResponse.model_validate(request)


@root_router.get("/request/{request_id}/")
async def get_request(request_id: int, session: AsyncSession = Depends(get_session)) -> RequestResponse:
    request = await request_service.get_request(session, request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    return RequestResponse.model_validate(request)


@root_router.get("/request/{request_id}/resultFile/", response_model=None)
async def get_request_result_file(
    request_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:

    # request = await request_service.get_request(session, request_id)
    #
    # if not request:
    #     raise HTTPException(status_code=404, detail="Request not found")
    #
    #
    # filename = f"resultFile_{request_id}.{file.file_path.split('.')[-1]}"
    #
    # binary_file = io.BytesIO()
    # await file.download_to_memory(binary_file)
    #
    # file_bytes = binary_file.getvalue()
    # binary_file.close()
    #
    # return Response(
    #     content=file_bytes,
    #     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    #     headers={"Content-Disposition": f"inline; filename={filename}"},
    # )
