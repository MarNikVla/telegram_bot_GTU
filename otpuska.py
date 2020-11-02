import telebot
import main

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = main.bot
dbx = main.dbx


def get_otpuska_folder(query):
    bot.answer_callback_query(query.id)
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = main.get_folders(folder='/tg_bot/', name=query.data)
    folders = [folder for folder in folders if folder.name.startswith('График отпусков')]
    for folder in folders[-4:]:
        keyboard.row(
                telebot.types.InlineKeyboardButton(str(folder.name),
                                                   callback_data=str(folder.name)
                                                   )
            )
    bot.send_message(
        query.message.chat.id,
        'Выберите график:',
        reply_markup=keyboard
    )

def get_otpusk_file(query):
    bot.answer_callback_query(query.id)
    load_otpusk_file(query)
    send_otpusk_file(query)
    path_to_file = Path(BASE_DIR, query.data)
    path_to_file.unlink()

def load_otpusk_file(query, folder='/tg_bot/Отпуска'):
    path_to_file = Path(BASE_DIR, query.data)
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + query.data
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)


def send_otpusk_file(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, query.data)
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )