import os
import time

import telebot
import re

from pathlib import Path
import grafiki, tables, otpuska, collectivniy_dogovor, common

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = common.bot
dbx = common.dbx


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: True, content_types=['text'])
def commands(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders()
    for folder in folders:
        keyboard.row(
            telebot.types.InlineKeyboardButton(folder.name, callback_data=folder.name)
        )
    bot.send_message(
        message.chat.id,
        'Выберите папку:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: bool(re.search('графики смен', call.data)))
def get_grafiki_folder(query):
    grafiki.get_grafiki_folder(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('графики год\s\w', call.data)))
def get_grafiki_year(query):
    grafiki.get_grafiks_result(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('график\s\w', call.data)))
def get_grafik_file(query):
    grafiki.get_grafik_file(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('Отпуска', call.data)))
def get_otpuska_folder(query):
    otpuska.get_otpuska_folder(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('График отпусков\s\d+', call.data)))
def get_otpusk_file(query):
    otpuska.get_otpusk_file(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('ТАБЕЛЯ', call.data)))
def get_tables_folder(query):
    tables.get_tables_folder(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('(Т|т)абеля\s\d+', call.data)))
def get_tables_result(query):
    tables.get_tables_result(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('табель\s\w+', call.data)))
def get_table_file(query):
    tables.get_table_file(query)


@bot.callback_query_handler(func=lambda call: bool(re.search('Коллективный\s\w+', call.data)))
def get_dogovor_file(query):
    collectivniy_dogovor.send_dogovor_file(query)


while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)

# bot.polling(none_stop=True)

