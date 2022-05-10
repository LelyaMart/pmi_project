import asyncio
from io import BytesIO

import requests
import telebot
from PIL import Image
from telebot import types

from db import top, update_results, update_users
from dclass import clas
from face_number import face_number
from tryToken import TOKEN

token = TOKEN
bot = telebot.TeleBot(token)
APP_NAME = 'Pmi_project'
blackList = set()

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_info = types.KeyboardButton('Info')
button_top = types.KeyboardButton('Топ преподавателей')
markup.add(button_info, button_top)


async def newPhoto(message):
    user_id = message.from_user.id
    username = message.from_user.username
    bot.send_message(message.from_user.id, "Секунду...")
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    path = 'https://api.telegram.org/file/bot' + token + '/' + file.file_path
    try:
        number = face_number(path)
    except:
        number = 0
        result = -1
    if number == 0:
        bot.send_message(message.from_user.id, "Ой, я не нашёл твоё лицо( Отправь мне другую фотографию")
        result = -1
    elif number == 1:
        try:
            x = clas(path)
            result = x[2]
            imag = requests.get(x[1]).content
            imag = Image.open(BytesIO(imag))
            bot.send_photo(message.from_user.id, imag,
                           caption="Преподаватель, который больше всего похож на человека с фото: " + x[2] + "\n" + x[
                               4])
            bot.send_message(message.from_user.id,
                             "Вот что я смог найти) Ты можешь отправить мне новую фотографию или проверить топ")
            update_results(result)
        except Exception:
            bot.send_message(message.from_user.id, "Ой, я не нашёл твоё лицо( Отправь мне другую фотографию")
            result = -1
    else:
        bot.send_message(message.from_user.id,
                         'На этой фотографии больше одного человека. Пожалуйста, отправь другое фото или обрежь это.')
        result = -1
    update_users(user_id, username, result)


def write_top(message):
    text = "Топ 5 часто выдаваемых преподавателей:\n"
    data = top()
    for i in data:
        text = text + str(i[0]) + " - " + str(i[1]) + " (совпадений)\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Привет! Отправь мне фотографию, и я скажу на какого преподавателя МИФИ ты похож.',
                     reply_markup=markup)


@bot.message_handler(
    content_types=['text', 'entities', 'audio', 'document', 'sticker', 'video', 'voice', 'caption', 'contact',
                   'location', 'venue', 'video_note'])
def get_text_messages(message):
    if message.text == 'Info':
        bot.send_message(message.from_user.id,
                         "Я - бот похожих преподавателей НИЯУ МИФИ. Если ты отправишь мне фотографию, то в ответ получишь того сотрудника нашего института, который больше всего похож на тебя. Алгоритм является экспериментальным, поэтому я могу иногда ошибаться. Также ты можешь посмотреть, какие из преподавателей встречаются чаще всего. Для этого отправь мне сообщение 'Топ преподавателей'")
    elif message.text == 'Топ преподавателей':
        write_top(message)
    else:
        bot.send_message(message.from_user.id, "Прости, я тебя не понимаю( Отправь мне фотографию")


@bot.message_handler(content_types=['photo'])
def getPhoto(message):
    if message.media_group_id:
        if message.from_user.id not in blackList:
            blackList.add(message.from_user.id)
            bot.send_message(message.from_user.id, "Давай не так быстро... Отправь мне фотографии по одной, пожалуйста")
    else:
        if message.from_user.id in blackList:
            blackList.remove(message.from_user.id)
        asyncio.run(newPhoto(message))


def main():
    try:
        bot.polling(none_stop=True)
    except Exception:
        main()


if __name__ == '__main__':
    main()
