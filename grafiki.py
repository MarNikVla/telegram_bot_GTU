
import telebot
import main

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = main.bot
dbx = main.dbx


def get_grafiks_folder(query):
    bot.answer_callback_query(query.id)
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = main.get_folders(folder='/tg_bot/', name=query.data)
    for folder in folders[-4:]:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name),
                                               callback_data=str(folder.name)
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        'Выберите папку с графиками:',
        reply_markup=keyboard
    )


def get_grafiks_result(query):
    bot.answer_callback_query(query.id)
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = main.get_folders(folder='/tg_bot/графики смен', name=query.data)
    for folder in folders:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name + ' ' + query.data),
                                               callback_data=str(folder.name) + ' ' + str(query.data[-4:])
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        str(query.data),
        reply_markup=keyboard
    )


def get_grafik_file(query):
    bot.answer_callback_query(query.id)
    load_grafik(query)
    send_grafik(query)
    path_to_file = Path(BASE_DIR, query.data[-4:] + query.data[:-4])
    path_to_file.unlink()


def load_grafik(query, folder='/tg_bot/графики смен'):
    path_to_file = Path(BASE_DIR, query.data[-4:] + query.data[:-4])
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + query.message.text + '/' + query.data[:-5]
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)


def send_grafik(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, query.data[-4:] + query.data[:-4])
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )
