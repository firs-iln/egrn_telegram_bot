from telegram import Update
from telegram.ext import ContextTypes

from .abstract_middleware import AbstractMiddleware


class ArqMiddleware(AbstractMiddleware):
    def __init__(self, arq=None):
        self.arq = arq

    def update_arq_app(self, arq):
        self.arq = arq

    async def on_update(self, update: Update, context: ContextTypes):
        context.__setattr__('arq_app', self.arq)

    async def after_update(self, update: Update, context: ContextTypes):
        pass
