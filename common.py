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


def get_folders(folder='/tg_bot/', name=''):
    enteries = sorted(dbx.files_list_folder(path=str(folder + '/' + name))._entries_value,
                      key=lambda i: i.name.lower())
    return enteries
