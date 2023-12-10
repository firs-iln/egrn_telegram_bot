import logging
from telegram import Update
from telegram.ext import ContextTypes
from .abstract_middleware import AbstractMiddleware
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker


class SessionMiddleware(AbstractMiddleware):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker
        self.logger = logging.getLogger(__name__)

    async def on_update(self, update: Update, context: ContextTypes):
        session = self.session_maker()
        context.__setattr__('session', session)

    async def after_update(self, update: Update, context: ContextTypes):
        try:
            session: AsyncSession = context.__getattribute__('session')
        except AttributeError:
            self.logger.warning('SessionMiddleware: session is not found in context')
        else:
            if session:
                # await session.commit()
                await session.close()
                context.__delattr__('session')
                self.logger.debug('SessionMiddleware: session is closed')
