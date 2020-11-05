import telebot
import common

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = common.bot
dbx = common.dbx


def get_tables_folder(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders(folder='/tg_bot/', name=query.data)
    folders = [folder for folder in folders if (folder.name.startswith('Табеля') or folder.name.startswith('табеля'))]

    for folder in folders[-3:]:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name),
                                               callback_data=str(folder.name)
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        'Выберите папку с табелями:',
        reply_markup=keyboard
    )


def get_tables_result(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders(folder='/tg_bot/ТАБЕЛЯ', name=query.data)
    folders = [folder for folder in folders if
               folder.name.startswith('табель') and len(folder.name.replace('ГТЦ', '')) < 22 and hasattr(folder, 'client_modified')]
    folders.sort(key=lambda i: i.client_modified)
    for folder in folders:
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name + ' ' + query.data),
                                               callback_data=str(folder.name[:26])
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        str(query.data),
        reply_markup=keyboard
    )


def get_table_file(query):
    load_table_file(query)
    send_table_file(query)
    path_to_file = Path(BASE_DIR, query.data)
    path_to_file.unlink()


def load_table_file(query, folder='/tg_bot/ТАБЕЛЯ'):
    path_to_file = Path(BASE_DIR, query.data)
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + query.message.text + '/' + query.data
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)


def send_table_file(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, query.data)
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )
