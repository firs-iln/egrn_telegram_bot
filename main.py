from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

# from api.routes import root_router
# from config import config
from logging import getLogger
from bot import telegram_app

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator[None, None]:
    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()

    logger.info('Telegram bot started')

    yield

    await telegram_app.updater.stop()
    await telegram_app.stop()
    await telegram_app.shutdown()

    logger.info('Telegram bot stopped')


def build_app() -> FastAPI:
    fast_api_app = FastAPI(lifespan=lifespan)
    # fast_api_app.include_router(root_router)

    return fast_api_app


app = build_app()
