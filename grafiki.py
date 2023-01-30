import telebot
import common

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = common.bot
dbx = common.dbx


def get_grafiki_folder(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders(folder='/tg_bot/', name=query.data)
    for i, folder in enumerate(folders[-3:]):
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name),
                                               callback_data='графики год' + ' ' + str(i)
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        'Выберите папку с графиками:',
        reply_markup=keyboard
    )


def get_grafiks_result(query):
    folder_index = int(query.data.split()[-1])
    folder = query.message.reply_markup.keyboard[folder_index][0].text
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders(folder='/tg_bot/графики смен', name=folder)
    files = [file for file in folders if
             (hasattr(file, 'client_modified') and file.name.endswith('xlsx'))]
    files.sort(key=lambda i: i.client_modified)
    for i, file in enumerate(files):
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(file.name),
                                               callback_data='график' + ' ' + folder + ' ' + str(i)
                                               )
        )
    bot.send_message(
        query.message.chat.id,
        str(folder),
        reply_markup=keyboard
    )


def get_grafik_file(query):
    folder = ' '.join(query.data.split()[-3:-1])
    file_index = int(query.data.split()[-1])
    file = query.message.reply_markup.keyboard[file_index][0].text
    bot.send_chat_action(query.message.chat.id, 'typing')
    load_grafik(folder, file)
    send_grafik(query, folder, file)
    path_to_file = Path(BASE_DIR, file)
    path_to_file.unlink()


def load_grafik(folder, file, main_folder='/tg_bot/графики смен'):
    path_to_file = Path(BASE_DIR, file)
    with open(path_to_file, 'wb') as f:
        db_path = main_folder + '/' + folder + '/' + file
        metadata, file = dbx.files_download(db_path)
        f.write(file.content)


def send_grafik(query, folder, file):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, file)
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f, caption=file[15:] + ' ' + folder[-4:]
    )
