from pprint import pprint

import telebot
import dropbox
import re

from pathlib import Path


DB_TOKEN = "RfH15ItBqVcAAAAAAAAAAYaswJ3ZlkUbgdAQhW48JTssGkQ_Vs4mI6xtDtWPoQjN"
TG_TOKEN = "1161497067:AAFI0BAYtaA2Z4Q97OCgQeKtGlxJv9gc7AI"
BASEDIR = Path(__file__).resolve(strict=True).parent

bot = telebot.TeleBot(TG_TOKEN)
dbx = dropbox.Dropbox(DB_TOKEN)

def load_file(query, folder='/tg_bot/графики смен'):
    path_to_file = Path(BASEDIR, query.data)
    # path_to_file = Path(BASEDIR, query.data[-4:] + query.data[:-4])
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + query.message.text + '/' + query.data[:-5]
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)


def get_folders(folder='/tg_bot/графики смен', name=''):
    enteries = sorted(dbx.files_list_folder(path=str(folder + '/' + name))._entries_value, key=lambda i: i.name)
    return enteries


@bot.message_handler(commands=['start'])
def commands(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = get_folders()
    for folder in folders[-3:]:
        keyboard.row(
            telebot.types.InlineKeyboardButton(folder.name, callback_data=folder.name)
        )
    bot.send_message(
        message.chat.id,
        'Выберите папку с графиками:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: bool(re.search('^графики\s\d+', call.data)))
def get_grafiks(query):
    bot.answer_callback_query(query.id)
    print(query.message)
    send_grafiks_result(query.message, query.data)


@bot.callback_query_handler(func=lambda call: True)
def get_file(query):
    bot.answer_callback_query(query.id)
    print(22)
    load_file(query)
    send_file_result(query)


def send_file_result(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASEDIR, query.data[-4:] + query.data[:-4])
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )
    # os.remove(path_to_file)


def send_grafiks_result(message, data):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = get_folders(name=data)
    for folder in folders:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name + ' ' + data),
                                               callback_data=str(folder.name) + ' ' + str(data[-4:])
                                               )
        )
    bot.send_message(
        message.chat.id,
        str(data),
        reply_markup=keyboard
    )


bot.polling()
