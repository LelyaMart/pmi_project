import telebot
from telebot import types
from dclass import clas
import requests
from io import BytesIO
from PIL import Image
from csvutil import *
import csv
from face_number import face_number
from ourToken import TOKEN

token = TOKEN
bot = telebot.TeleBot(token)
APP_NAME = 'Pmi_project'

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_info = types.KeyboardButton('Info')
button_top = types.KeyboardButton('Топ преподавателей')
markup.add(button_info, button_top)

def write_top(message):
    text = "Топ 5 часто выдаваемых преподавателей:\n"
    with open('top.csv') as topfile:
        array = [r for r in csv.reader(topfile, delimiter=' ')]
        array.pop(0)
        for i in range(5):
            text = text + array[i][0] + " - " + array[i][1] + " (совпадений)\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Отправь мне фотографию, и я скажу на какого преподавателя МИФИ ты похож.', reply_markup= markup)

@bot.message_handler(content_types=['text', 'entities', 'audio', 'document', 'sticker', 'video', 'voice', 'caption', 'contact', 'location', 'venue'])
def get_text_messages(message):
    if message.text == 'Info':
        bot.send_message(message.from_user.id, "Я - бот похожих преподавателей НИЯУ МИФИ. Если ты отправишь мне фотографию, то в ответ получишь того сотрудника нашего института, который больше всего похож на тебя. Алгоритм является экспериментальным, поэтому я могу иногда ошибаться. Также ты можешь посмотреть, какие из преподавателей встречаются чаще всего. Для этого отправь мне сообщение 'Топ преподавателей'")
    elif message.text == 'Топ преподавателей':
        write_top(message)
    else:
        bot.send_message(message.from_user.id, "Прости, я тебя не понимаю( Отправь мне фотографию")

@bot.message_handler(content_types=['photo'])
def getPhoto(message):
    user_id = message.from_user.id
    username = message.from_user.username
    bot.send_message(message.from_user.id, "Секунду...")
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    path = file.file_path
    path = 'https://api.telegram.org/file/bot' + token + '/' + path
    try:
        face_number(path)
    except Exception as e:
          bot.send_message(message.from_user.id, e)
    if face_number(path) <= 1:
        try:
            x = clas(path)
            result = x[2]
            imag = requests.get(x[1]).content
            imag = Image.open(BytesIO(imag))
            bot.send_photo(message.from_user.id, imag, caption = "Преподаватель, который больше всего похож на человека с фото: " + x[2] + "\n" + x[4])
            bot.send_message(message.from_user.id, "Вот что я смог найти) Ты можешь отправить мне новую фотографию или проверить топ")
            write_result_to_csv(result)
        except Exception as e:
            print(e)
            bot.send_message(message.from_user.id, "Ой, я не нашёл твоё лицо( Отправь мне другую фотографию")
            result = -1
    else:
        bot.send_message(message.from_user.id, 'На этой фотографии больше одного человека. Пожалуйста, отправь другое фото или обрежь это.')
        result = -1
    write_id_to_csv(user_id, username, result)


def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        main()

if __name__ == '__main__':
    main()

