from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes


class AbstractMiddleware(ABC):
    @abstractmethod
    async def on_update(self, update: Update, context: ContextTypes):
        pass

    @abstractmethod
    async def after_update(self, update: Update, context: ContextTypes):
        pass
