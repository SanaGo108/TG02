import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from config import TOKEN, OPENWEATHER_API_KEY

import random

from gtts import gTTS
import os

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_weather(city: str) -> str:
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            data = await response.json()
            if response.status == 200:
                description = data['weather'][0]['description']
                temp = data['main']['temp']
                return f"Погода в {city}: {description}, температура: {temp}°C"
            else:
                return "Не удалось получить прогноз погоды. Попробуйте позже."

@dp.message(Command('weather'))
async def weather(message: Message):
    weather_report = await get_weather("Москва")
    await message.answer(weather_report)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile("video-priroda.mp4")
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("audio_2.ogg")
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("White.pdf")
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile("audio.mp3")
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1: Скручивания: 3 подхода по 15 повторений. Велосипед: 3 подхода по 20 повторений (каждая сторона). Планка: 3 подхода по 30 секунд",
        "Тренировка 2: Подъемы ног: 3 подхода по 15 повторений. Русский твист: 3 подхода по 20 повторений (каждая сторона). Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3: Скручивания с поднятыми ногами: 3 подхода по 15 повторений. Горизонтальные ножницы: 3 подхода по 20 повторений. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f"Это ваша мини тренировка на сегодня: {rand_tr}")

    tts = gTTS(text=rand_tr, lang='ru')
    tts.save("training.ogg")
    audio = FSInputFile('training.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove("training.ogg")

@dp.message(Command('photo'))
async def photo(message:Message):
    list1 = ['https://zavera.rs/wp-content/uploads/2021/06/mozak-kovid.jpg', 'https://img.freepik.com/fotos-premium/formacao-medica-3d-com-cabeca-masculina-e-cerebro-em-fios-de-dna_974732-7410.jpg', 'https://www.teamlewis.com/es/wp-content/uploads/sites/15/2018/08/BannerPrincipal.jpg']
    rand_photo = random.choice(list1)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Не понятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message:Message):
    await message.answer('Иску́сственный интелле́кт (англ. artificial intelligence; AI) в самом '
                         'широком смысле – это интеллект, демонстрируемый машинами, в частности'
                         ' компьютерными системами. Это область исследований в области компьютерных'
                         ' наук, которая разрабатывает и изучает методы и программное обеспечение, '
                         'позволяющие машинам воспринимать окружающую среду и использовать обучение'
                         ' и интеллект для выполнения действий, которые максимально увеличивают их '
                         'шансы на достижение поставленных целей[1]. Такие машины можно назвать '
                         'искусственным интеллектом.')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Этот бот умеет выполнять команды: \n /start \n /help \n /photo \n /weather')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}')

@dp.message()
async def start(message: Message):
    if message.text.lower() == 'test':
        await message.answer('Тестируем')


async def main():
    await dp.start_polling(bot)

if __name__== '__main__':
    asyncio.run(main())