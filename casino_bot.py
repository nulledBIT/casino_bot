from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes
import logging
import asyncio
import random
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token='1372640546:AAGpBHUljMNvhJgfcNb9jZPhH_y53D97ALw')
dp = Dispatcher(bot)
game_started = False
players = []


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'Ы')


@dp.message_handler(commands=['new_game'])
async def start_game(message: types.Message):
    global game_started, players
    if game_started:
        await bot.send_message(message.chat.id, 'Игра уже запущена, если хотите создать новую сначала ипользуйте /reset')
        return
    players = []
    game_started = True
    await bot.send_message(message.chat.id, 'Началась запись на игру. Чтобы записаться напиши в чате /addme в ответ на сообщение бота')


@dp.message_handler(commands=['addme'])
async def plus_1(message: types.Message):
    global game_started, players
    if not game_started:
        await bot.send_message(message.chat.id, 'Игра еще не создана, используйте /new_game')
        return
    try:
        if message.reply_to_message.from_user.bot:
            if message.from_user.username is None:
                await bot.send_message(message.chat.id, 'Для учатия нужен username')
                return
            if message.from_user.username in players:
                await bot.send_message(message.chat.id, 'Вы уже присоединились')
                return
            players.append(message.from_user.username)
            await bot.send_message(message.chat.id, 'Вы присоединились')
    except:
        print(123)


@dp.message_handler(commands=['reset'])
async def reset(message: types.Message):
    global game_started
    game_started = False
    await bot.send_message(message.chat.id, 'Reset')


@dp.message_handler(commands=['go'])
async def game(message: types.Message):
    global game_started, players
    if not game_started:
        await bot.send_message(message.chat.id, 'Игра еще не создана, используйте /new_game')
    if players == []:
        await bot.send_message(message.chat.id, 'Нужен хоть 1 игрок')
        return
    await bot.send_message(message.chat.id, 'Выиграл @'+str(random.choice(players)))

if __name__ == '__main__':
    executor.start_polling(dp)
