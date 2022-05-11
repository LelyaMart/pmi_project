import asyncio
from io import BytesIO

import requests
from PIL import Image
from telebot.async_telebot import AsyncTeleBot  # нужна последняя версия pyTelegramBotAPI
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

import api
from db import top, update_results, update_users
from dclass import clas
from face_number import face_number
from tryToken import TOKEN

token = TOKEN
bot = AsyncTeleBot(token)
queue = asyncio.Queue()
APP_NAME = 'Pmi_project'
blackList = set()

markup = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton('Info')
button_top = KeyboardButton('Топ преподавателей')
markup.add(button_info, button_top)


def get_numpy_array_from_network(url):
    decode_image = BytesIO(requests.get(url).content)
    return api.load_image_file(decode_image)


async def newPhoto(message: Message):
    # await bot.send_message(message.from_user.id, "Секунду...")
    fileID = message.photo[-1].file_id
    file = await bot.get_file(fileID)
    fileUrl = 'https://api.telegram.org/file/bot' + token + '/' + file.file_path
    image_numpy_array = get_numpy_array_from_network(fileUrl)
    face_count = face_number(image_numpy_array)
    result = -1
    if face_count == 0:
        await bot.reply_to(message, "Ой, я не нашёл твоё лицо( Отправь мне другую фотографию")
    elif face_count == 1:
        try:
            row_data = clas(image_numpy_array)
            result = row_data[2]
            teacher_image_url = row_data[1]
            teacher_image = Image.open(BytesIO(requests.get(teacher_image_url).content))
            await bot.send_photo(message.from_user.id, teacher_image, caption=f"Преподаватель, который больше всего похож на человека с фото: {row_data[2]}\n{row_data[4]}")
            await bot.reply_to(message, "Вот что я смог найти) Ты можешь отправить мне новую фотографию или проверить топ")
            update_results(result)
        except Exception as e:
            print(e)
            await bot.reply_to(message, "Ой, я не нашёл твоё лицо( Отправь мне другую фотографию")
    else:
        await bot.reply_to(message, 'На этой фотографии больше одного человека. Пожалуйста, отправь другое фото или обрежь это.')
    update_users(message.from_user.id, message.from_user.username, result)


async def write_top(message):
    text = "Топ 5 часто выдаваемых преподавателей:\n"
    data = top()
    for i in data:
        text = text + str(i[0]) + " - " + str(i[1]) + " (совпадений)\n"
    await bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(message.chat.id,
                           'Привет! Отправь мне фотографию, и я скажу на какого преподавателя МИФИ ты похож.',
                           reply_markup=markup)


@bot.message_handler(content_types=['text', 'entities', 'audio', 'document', 'sticker', 'video', 'voice', 'caption', 'contact', 'location', 'venue', 'video_note'])
async def get_text_messages(message):
    if message.text == 'Info':
        await bot.send_message(message.from_user.id,
                               "Я - бот похожих преподавателей НИЯУ МИФИ. Если ты отправишь мне фотографию, то в ответ получишь того сотрудника нашего института, который больше всего похож на тебя. Алгоритм является экспериментальным, поэтому я могу иногда ошибаться. Также ты можешь посмотреть, какие из преподавателей встречаются чаще всего. Для этого отправь мне сообщение 'Топ преподавателей'")
    elif message.text == 'Топ преподавателей':
        await write_top(message)
    else:
        await bot.send_message(message.from_user.id, "Прости, я тебя не понимаю( Отправь мне фотографию")


@bot.message_handler(content_types=['photo'])
async def getPhoto(message: Message):
    if message.media_group_id:
        if message.from_user.id not in blackList:
            blackList.add(message.from_user.id)
            await bot.reply_to(message, "Давай не так быстро... Отправь мне фотографии по одной, пожалуйста")
    else:
        if message.from_user.id in blackList:
            blackList.remove(message.from_user.id)
        if queue.qsize() == 500:
            await bot.reply_to(message, f"Подождите, в очереди слишком много запросов.\nПовторите попытку позже.")
        else:
            await queue.put(message)
            await bot.reply_to(message, f"Подождите, в очереди {queue.qsize()} запросов.")


async def worker() -> None:
    while True:
        message = await queue.get()
        await newPhoto(message)


def main():
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(bot.polling())
        loop.run_until_complete(worker())
    except Exception as e:
        print(e)
        main()


if __name__ == '__main__':
    main()
