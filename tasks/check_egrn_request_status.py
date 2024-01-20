async def check_egrn_request_status(cntx, chat_id: int | str) -> None:
    from bot import telegram_app

    await telegram_app.bot.send_message(
        chat_id=chat_id,
        text="Прошло скока то времени лалала",
    )
