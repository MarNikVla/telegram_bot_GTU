import os

import dotenv
import telebot
import dropbox

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

# Загружаем виртуальное окружение из .env если он существует смотри .env
dotenv_file = Path(BASE_DIR, ".env")
if Path.is_file(dotenv_file):
    dotenv.load_dotenv(dotenv_file)


DB_TOKEN = os.getenv("DB_TOKEN")
TG_TOKEN = os.getenv("TG_TOKEN")


bot = telebot.TeleBot(TG_TOKEN)
dbx = dropbox.Dropbox(DB_TOKEN)

def get_folders(folder='/tg_bot/графики смен', name=''):
    enteries = sorted(dbx.files_list_folder(path=str(folder + '/' + name))._entries_value, key=lambda i: i.name)
    return enteries

def load_file(query, folder='/tg_bot/графики смен'):
    # path_to_file = Path(BASEDIR, query.data)
    path_to_file = Path(BASE_DIR, query.data[-4:] + query.data[:-4])
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + query.message.text + '/' + query.data[:-5]
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)

def send_file(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, query.data[-4:] + query.data[:-4])
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )