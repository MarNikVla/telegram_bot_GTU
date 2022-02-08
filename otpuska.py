import telebot
import common

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

bot = common.bot
dbx = common.dbx


def get_otpuska_folder(query):
    bot.send_chat_action(query.message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=4)
    folders = common.get_folders(folder='/tg_bot/', name=query.data)
    files = [files for files in folders if files.name.startswith('График отпусков')]

    for index, folder in enumerate(files[-4:]):
        keyboard.row(
            telebot.types.InlineKeyboardButton(str(folder.name),
                                               callback_data='График отпусков' + ' ' + str(index)
                                               ))

    bot.send_message(
        query.message.chat.id,
        'Выберите график отпусков:',
        reply_markup=keyboard
    )


def get_otpusk_file(query):
    file_index = int(query.data.split()[-1])
    file = query.message.reply_markup.keyboard[file_index][0].text
    path_to_file = Path(BASE_DIR, file)

    load_otpusk_file(file)
    send_otpusk_file(query, file)

    path_to_file.unlink()


def load_otpusk_file(file, folder='/tg_bot/Отпуска'):
    path_to_file = Path(BASE_DIR, file)
    with open(path_to_file, 'wb') as f:
        db_path = folder + '/' + file
        metadata, db_file = dbx.files_download(db_path)
        f.write(db_file.content)


def send_otpusk_file(query, file):
    bot.send_chat_action(query.message.chat.id, 'typing')
    path_to_file = Path(BASE_DIR, file)
    f = open(path_to_file, 'rb')
    bot.send_document(
        query.message.chat.id, f,
    )
