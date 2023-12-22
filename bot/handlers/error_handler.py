import logging
import traceback
import html

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

TELEGRAM_LOGS_CHAT_ID = 280584516


async def send_stacktrace_to_tg_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>{html.escape(tb_string)[:4080]}</pre>'
    )

    user_message = 'К сожалению произошла внутренняя ошибка. Пожалуйста, попробуйте ещё раз позднее...'

    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=user_message,
        )

    admin_message = f"{message}"
    if TELEGRAM_LOGS_CHAT_ID:
        await context.bot.send_message(
            chat_id=TELEGRAM_LOGS_CHAT_ID,
            text=admin_message,
            parse_mode="HTML",
        )
    else:
        logger.error(admin_message)
