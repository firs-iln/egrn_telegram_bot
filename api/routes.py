from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import HTTPException
from starlette.responses import Response

from api.deps import get_session

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

from crud import request as request_service
from crud import user as user_service
from schemas.request import RequestCreate, RequestResponse
from schemas.user import UserCreate, UserResponse

from bot import telegram_app
from sqlalchemy.ext.asyncio import AsyncSession
import io

from .types import OrderCallbackInput

from client_server_api import client_server_api

from bot.parser.parse_website.util import Parser

from bot.parser.tables.parse_xlsx import make_register_file

root_router = APIRouter(
    prefix="/api/v1/request",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

bot: Bot = telegram_app.bot


@root_router.post("/")
async def create_request(
        request_create: RequestCreate,
        session: AsyncSession = Depends(get_session),
) -> RequestResponse:
    request = await request_service.create_request(
        session, request_create
    )

    admin = await user_service.get_admins(session)
    admin = admin[0]

    markup = InlineKeyboardMarkup([[InlineKeyboardButton("Выписка МКД", callback_data=f"r1r7_start_{request.id}")]])

    await bot.send_message(
        chat_id=admin.id,
        text=f"Поступила новая заявка на кадастровый номер {request_create.cadnum}.\n",
        reply_markup=markup,
    )

    return RequestResponse.model_validate(request)


async def process_file(session: AsyncSession, request_id: int):
    request = await request_service.get_request(session, request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    src = request.r1r7_filename
    try:
        parser_obj = Parser(src)
        await parser_obj.process_objects()
    except Exception as e:
        parser_obj = Parser(src)
        await parser_obj.process_objects()

    doc, area = make_register_file(src)
    request.registry_filename = doc

    admin = await user_service.get_admins(session)
    admin = admin[0]

    if not request.fio_is_provided:
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"Отправить результат", callback_data=f"registry_confirm_{request.id}"),
            InlineKeyboardButton(f"Внести изменения", callback_data=f"registry_edit_{request.id}"),
        ]])
        reply = "Файл готов, отправить?"
    else:
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"Настроить колонки", callback_data=f"registry_insert_owners_{request.id}"),
            InlineKeyboardButton(f"Внести изменения", callback_data=f"registry_edit_{request.id}"),
        ]])
        reply = 'Требуется внесение ФИО в файл. Нажмите Настройка, чтобы продолжить'

    await bot.send_document(
        chat_id=admin.id,
        document=doc,
        caption=f"РеестрМКД по заказу {request.id}\n\nПлощадь КВ+НЖ+ММ = {area:.1f} кв.м.\n\n{reply}",
        reply_markup=markup,
    )

    await session.commit()


@root_router.post("/{request_id:int}/startProduction")
async def start_production(
        request_id: int,
        background_tasks: BackgroundTasks,
        session: AsyncSession = Depends(get_session),
) -> RequestResponse:
    request = await request_service.get_request(session, request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    background_tasks.add_task(process_file, session, request_id)

    return RequestResponse.model_validate(request)


@root_router.get("/{request_id:int}/r1r7/")
async def get_request(request_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    request = await request_service.get_request(session, request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    filename = request.r1r7_filename
    with open(filename, "rb") as file:
        file_bytes = file.read()

    return Response(
        content=file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"inline; filename=r1r7.xlsx"},
    )


@root_router.get("/{request_id:int}/registry/", response_model=None)
async def get_request_result_file(
        request_id: int,
        session: AsyncSession = Depends(get_session),
) -> Response:
    request = await request_service.get_request(session, request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    filename = request.registry_filename
    with open(filename, "rb") as file:
        file_bytes = file.read()

    return Response(
        content=file_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"inline; filename=registry.xlsx"},
    )
