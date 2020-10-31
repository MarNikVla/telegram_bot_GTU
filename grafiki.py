import os

import dotenv
import telebot
import dropbox
import re
import main

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent


bot = main.bot
dbx = main.dbx



def get_grafiks_result(query):
    bot.answer_callback_query(query.id)
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = main.get_folders(name=query.data)
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

@bot.callback_query_handler(func=lambda call: bool(re.search('\S+(xls|xlsx)\s+\d{3,}', call.data)))
def get_grafik_file(query):
    bot.answer_callback_query(query.id)
    main.load_file(query)
    main.send_file(query)


