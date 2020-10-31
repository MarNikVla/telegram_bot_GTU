import os

import telebot
import dropbox
import dotenv
import re

from pathlib import Path
import grafiki
import main

BASE_DIR = Path(__file__).resolve(strict=True).parent


bot = main.bot
dbx = main.dbx


@bot.message_handler(commands=['start'])
def commands(message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = main.get_folders()
    for folder in folders[-3:]:
        keyboard.row(
            telebot.types.InlineKeyboardButton(folder.name, callback_data=folder.name)
        )
    bot.send_message(
        message.chat.id,
        'Выберите папку с графиками:',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: bool(re.search('графики\s\d+', call.data)))
def get_grafiks(query):
    grafiki.get_grafiks_result(query)


bot.polling()
