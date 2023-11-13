import os
import pprint
import re
import zipfile

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, \
    CallbackQueryHandler
from telegram.ext.filters import TEXT, Document, COMMAND
from parser.parse_pdf import find_info, repr_info, check_pdf_to_be_valid_doc, get_floors_pics, floors, process_pdf

token = os.environ.get("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    egrn = KeyboardButton("ЕГРН")

    markup = ReplyKeyboardMarkup.from_button(egrn,
                                             input_field_placeholder='Выберите действие:',
                                             resize_keyboard=True)

    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                             text="Выберите действие из меню",
                                             reply_markup=markup)
    context.user_data['messages_to_delete'] = []
    context.user_data["messages_to_delete"].extend([message, update.message])
    return "egrn_chose"


async def egrn_chose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "ЕГРН":
        remove_markup = ReplyKeyboardRemove()
        message = await context.bot.send_message(update.message.chat.id, "Вставьте файл выписки на здание:",
                                                 reply_markup=remove_markup)
        context.user_data["messages_to_delete"].extend([message, update.message])
        return "get_doc"


async def get_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document)

    received_files_path = 'files/received/'

    message_to_reply = update.message

    document_name = update.message.document.file_name
    src = received_files_path + document_name
    await file.download_to_drive(src)

    if not document_name.endswith(".pdf"):  # file format check
        if not document_name.endswith("zip"):
            message = await update.message.reply_text("Неверный формат файла, попробуйте ещё раз")
            context.user_data["messages_to_delete"].extend([message, update.message])
            return

        with open(src, 'rb') as zip:
            if zipfile.is_zipfile(zip):
                z = zipfile.ZipFile(zip)
                for member in z.namelist():
                    if member.split('.')[-1] == 'pdf':
                        z.extract(member=member, path=received_files_path)
                        new_name = find_info(received_files_path + member)
                        new_name = ' '.join(new_name.values()) + ".pdf"
                        src = received_files_path + new_name
                        os.rename(received_files_path + member, src)
                        message_to_reply = await context.bot.send_document(update.message.chat.id, src)
                        await update.message.delete()
                        break

    print(src)
    if not check_pdf_to_be_valid_doc(src):  # file contains some title
        message = await update.message.reply_text("Неверный формат файла, попробуйте ещё раз")
        context.user_data["messages_to_delete"].extend([message, update.message])
        os.remove(src)
        return

    context.user_data["src"] = src

    doc = process_pdf(src)

    cad = find_info(src)["Кадастровый номер"]

    floors_reply = floors(src)

    floors_file = f'{cad}.txt'
    with open(floors_file, 'wt', encoding='utf-8') as f:
        f.write(floors_reply)

    context.user_data["floors_file"] = floors_file

    pics = InlineKeyboardButton(text="Планы", callback_data="Планы")
    markup = InlineKeyboardMarkup.from_button(pics)

    await message_to_reply.reply_document(doc, quote=True)

    message = await context.bot.send_message(update.message.chat.id, floors_reply, reply_markup=markup)

    await delete_messages(context)
    context.user_data["messages_to_delete"].append(message)

    return "pics_chose"


async def pics_chose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    text = update.callback_query.data
    if text == "Планы":
        message = await context.bot.send_message(update.callback_query.message.chat.id,
                                                 "Введите номера листов для получения архива поэтажный планов: (через запятую или пробел)")
        context.user_data["messages_to_delete"].append(message)
        return "floor_pics"


async def floor_pics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    floors = re.split(', |,| ', update.message.text)
    src = context.user_data["src"]
    floors_filename = context.user_data.get("floors_file", None)
    res = get_floors_pics(src, floors, floors_filename)
    if res:
        egrn = KeyboardButton("ЕГРН")

        markup = ReplyKeyboardMarkup.from_button(egrn,
                                                 input_field_placeholder='Выберите действие:',
                                                 resize_keyboard=True)

        await context.bot.send_document(update.message.chat.id, res, reply_markup=markup)
        context.user_data["messages_to_delete"].append(update.message)
        await delete_messages(context)
    return 'wait'


async def delete_messages(context: ContextTypes.DEFAULT_TYPE):
    for message in context.user_data.get("messages_to_delete", []):
        await message.delete()
    context.user_data["messages_to_delete"] = []


if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            'egrn_chose': [MessageHandler(filters=TEXT & ~COMMAND, callback=egrn_chose)],
            'get_doc': [MessageHandler(filters=Document.ALL, callback=get_doc)],
            'pics_chose': [
                CallbackQueryHandler(pattern="Планы", callback=pics_chose),
            ],
            'floor_pics': [MessageHandler(filters=TEXT & ~COMMAND, callback=floor_pics)],
            'wait': [MessageHandler(filters=TEXT & ~COMMAND, callback=egrn_chose)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    app.add_handler(conversation_handler)

    app.run_polling()
