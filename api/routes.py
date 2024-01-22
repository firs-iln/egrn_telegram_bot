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
from bot.parser.parse_website.dadata_rep import dadata
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


def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param exceptions: Lists of exceptions that trigger a retry attempt
    :type exceptions: Tuple of Exceptions
    """

    def decorator(func):
        def new_fn(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(
                        'Exception thrown when attempting to run %s, attempt '
                        '%d of %d' % (func, attempt, times)
                    )
                    attempt += 1
            return func(*args, **kwargs)

        return new_fn

    return decorator


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

    address = dadata.get_clean_data_by_cadastral_number(request_create.cadnum)

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("reestr-api", callback_data=f"r1r7_from_api_{request.id}"),
                InlineKeyboardButton("Выписка МКД", callback_data=f"r1r7_start_{request.id}")
            ]
        ]
    )

    await bot.send_message(
        chat_id=admin.id,
        text=f"Новый заказ на РеестрМКД " + ("(с ФИО)" if request_create.fio_is_provided else "(без ФИО)") + "\n" + \
             f"Заказ № {request_create.order_id}\n" + \
             f"Кадномер: {request_create.cadnum}\n" + \
             f"Адрес: {address.result}",
        reply_markup=markup,
    )

    return RequestResponse.model_validate(request)


async def process_file(session: AsyncSession, request_id: int):
    @retry(2, [Exception])
    async def inner(src):
        parser_obj = Parser(src)
        await parser_obj.process_objects()

    request = await request_service.get_request(session, request_id)
    await session.refresh(request, ["id", "fio_is_provided"])

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    src = request.r1r7_filename

    await inner(src)

    doc, area = make_register_file(src)
    request.registry_filename = doc

    request.total_area = area

    admin = await user_service.get_admins(session)
    admin = admin[0]

    if not request.fio_is_provided:
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"Отправить результат", callback_data=f"registry_confirm_{request_id}"),
            InlineKeyboardButton(f"Внести изменения", callback_data=f"registry_edit_{request_id}"),
        ]])
        reply = "Файл готов, отправить?"
    else:
        markup = InlineKeyboardMarkup([[
            InlineKeyboardButton(f"Настроить колонки", callback_data=f"registry_insert_owners_{request_id}"),
            InlineKeyboardButton(f"Внести изменения", callback_data=f"registry_edit_{request_id}"),
        ]])
        reply = 'Требуется внесение ФИО в файл. Нажмите Настройка, чтобы продолжить'

    await bot.send_document(
        chat_id=admin.id,
        document=doc,
        caption=f"РеестрМКД по заказу {request_id}\n\nПлощадь КВ+НЖ+ММ = {area:.1f} кв.м.\n\n{reply}",
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
