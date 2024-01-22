from arq import Retry
from egrn_api import api as egrn_requests_api
from crud import request as request_service
from crud import user as user_service
from logging import getLogger
from database import engine
from database.enums import RequestStatusEnum

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


logger = getLogger(__name__)

session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

delays = {
    0: 15*60,
    1: 60*60 - 15*60,
    2: 2*60*60 - 60*60 - 15*60,
    3: 6*60*60 - 2*60*60 - 60*60 - 15*60,
    4: 25*60*60 - 6*60*60 - 2*60*60 - 60*60 - 15*60,
}


async def check_egrn_request_status(cntx, request_id: int) -> None:
    from bot import telegram_app

    attempt = cntx.get("job_try", 0)

    if attempt > 4:
        logger.error(f"Failed to check order status for request_id={request_id} after 4 attempts")
        return

    delay = delays[attempt]

    session = session_maker()

    request = await request_service.get_request(session, request_id)

    if not request:
        logger.error(f"Request with id={request_id} not found")
        return

    if request.status != RequestStatusEnum.WAITINGFOREXTRACT:
        logger.info(f"Request with id={request_id} is already processed")
        return

    response = await egrn_requests_api.check_order(request.reestr_api_order_id)

    if response is None:
        logger.error(f"Failed to check order status for request_id={request_id}")
        raise Retry(defer=delay)

    if not response.complete:
        logger.info(f"Order {request_id} is not complete yet")

        # await telegram_app.bot.send_message(
        #     848643556,
        #     f"Заказ {request_id} еще не готов",
        # )

        raise Retry(defer=delay)

    # await telegram_app.bot.send_message(
    #     848643556,
    #     f"Заказ {request_id} готов",
    # )

    download_file_response = await egrn_requests_api.download_order_file(request.reestr_api_order_id)

    if download_file_response is None:
        logger.error(f"Failed to download order file for request_id={request_id}")
        raise Retry(defer=delay)

    with open(f'files/received/{download_file_response.filename}', "wb") as f:
        f.write(download_file_response.file_bytes)

    await request_service.update_request(session, request_id,
                                         extract_filename=download_file_response.filename,
                                         status=RequestStatusEnum.EXTRACTDONE)

    admins = await user_service.get_admins(session)

    if not admins:
        logger.error("No admins found")
        raise Retry(defer=delay)

    admin = admins[0]

    text = f"Выписка для заказа №{request_id} готова."

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Изготовить Р1Р7",
                    callback_data=f"r1r7_start_{request_id}",
                )
            ]
        ]
    )

    await telegram_app.bot.send_document(
        chat_id=admin.id,
        document=download_file_response.file_bytes,
        filename=download_file_response.filename,
    )

    await telegram_app.bot.send_message(
        chat_id=admin.id,
        text=text,
        reply_markup=keyboard,
    )
