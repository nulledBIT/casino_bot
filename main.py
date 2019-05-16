import values
from battle import Battle
from user import GetUserData
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentTypes
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=values.token)
dp = Dispatcher(bot)


@dp.message_handler(lambda message:message.text and not GetUserData(message.from_user.id).get_user_state())
async def check_registration(message: types.Message):
    if message.from_user.username is None:
        await bot.send_message(message.chat.id, 'Для начала работы с ботом вы должны указать имя пользователя(username) в настройках(Например - @username)')
        return
    user = GetUserData(message.from_user.id)
    user.new_profile(message.from_user.username)
    await bot.send_message(message.chat.id, 'Приветствую тебя в Little RPG', reply_markup=user.get_buttons_by_location())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.username is None:
        await bot.send_message(message.chat.id, 'Для начала работы с ботом вы должны указать имя пользователя(username) в настройках(Например - @username)')
        return
    user = GetUserData(message.from_user.id)
    await bot.send_message(message.chat.id, 'С возвращением', reply_markup=user.get_buttons_by_location())


@dp.message_handler(lambda message:message.text and message.text == "Бой")
async def battle(message: types.Message):
    user = GetUserData(message.from_user.id)
    location = user.get_location()
    if location[0] != 'Овраг':
        await bot.send_message(message.chat.id, 'Вы должны находитья в Овраге', reply_markup=user.get_buttons_by_location())
        return
    bat = Battle(message.from_user.id, 1)
    bat.get_user_battle_data()
    bat.get_mob_battle_data()
    battle_result = bat.fight()
    await bot.send_message(message.chat.id, battle_result, reply_markup=user.get_buttons_by_location())


@dp.message_handler(lambda message:message.text and message.text == 'Локации')
async def locations_list(message: types.Message):
    user = GetUserData(message.from_user.id)
    location = user.get_location()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Овраг')
    btn2 = types.KeyboardButton('Лесное поселение')
    markup.add(btn1, btn2)
    await bot.send_message(message.chat.id, 'Вы находитесь в: {}\nВыберите пункт назначения'.format(location[0]), reply_markup=markup)


@dp.message_handler(lambda message:message.text and message.text == 'Овраг')
async def go_to_ovrag(message: types.Message):
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    location_target = 'Овраг'
    user = GetUserData(message.from_user.id)
    location = user.get_location()
    if location[0] != 'Овраг':
        curs.execute("UPDATE profiles SET location = '{1}' WHERE id = {0}".format(message.from_user.id, location_target))
        conn.commit()
        conn.close()
        await bot.send_message(message.chat.id, 'Вы отправились в: {}. Прибудете через 10 секунд'.format(location_target), reply_markup=user.get_buttons_by_location())
        await asyncio.sleep(10)
        await bot.send_photo(message.chat.id, photo='AgADAgADQKoxG8Hv6ErQydsgk1vT2FxHOQ8ABDInYJlNENyunqoFAAEC')
        await bot.send_message(message.chat.id, 'Вы прибыли в: {}'.format(location_target), reply_markup=user.get_buttons_by_location())
    else:
        await bot.send_message(message.chat.id, 'Вы уже находитесь в: {}'.format(location[0]), reply_markup=user.get_buttons_by_location())


@dp.message_handler(lambda message:message.text and message.text == 'Лесное поселение')
async def go_to_poselok(message: types.Message):
    conn = sqlite3.connect('main.db')
    curs = conn.cursor()
    location_target = 'Лесное поселение'
    user = GetUserData(message.from_user.id)
    location = user.get_location()
    if location[0] != 'Лесное поселение':
        curs.execute("UPDATE profiles SET location = '{1}' WHERE id = {0}".format(message.from_user.id, location_target))
        conn.commit()
        conn.close()
        await bot.send_message(message.chat.id, 'Вы отправились в: {}. Прибудете через 10 секнд'.format(location_target), reply_markup=user.get_buttons_by_location())
        await asyncio.sleep(10)
        await bot.send_photo(message.chat.id, photo='AgADAgADt6oxG8Hv4EpnYtsFEpF7NODTUQ8ABGFJJpmCwdUMDVADAAEC')
        await bot.send_message(message.chat.id, 'Вы прибыли в: {}'.format(location_target), reply_markup=user.get_buttons_by_location())
    else:
        await bot.send_message(message.chat.id, 'Вы уже находитесь в: {}'.format(location[0]), reply_markup=user.get_buttons_by_location())




@dp.message_handler(lambda message:message.text and message.text == 'Профиль')
async def get_profile(message: types.Message):
    user = GetUserData(message.from_user.id)
    user_profile = user.get_user()
    profile = values.profile_text.format(user_profile[0], user_profile[1], user_profile[2], user_profile[3], user_profile[4], user_profile[5], user_profile[6], user_profile[7], user_profile[8], user_profile[9], user_profile[10])
    await bot.send_message(message.chat.id, profile, reply_markup=user.get_buttons_by_location())


@dp.message_handler(commands=["map"])
async def map(message: types.Message):
    user = GetUserData(message.from_user.id)
    await bot.send_photo(message.chat.id, photo="AgADAgAD4KwxGzOw6ErZpEH39TGkoyGwhQ8ABFg74t_vEBYoVg0AAgI", reply_markup=user.get_buttons_by_location())


@dp.message_handler( lambda message:message.text and message.from_user.id in values.admins, commands=["get_db"])
async def get_db(message: types.Message):
    if message.text[8:] == 'text':
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM profiles')
        await bot.send_message(message.chat.id, str(curs.fetchall()))
        curs.execute('SELECT * FROM mobs')
    else:
        doc = open('main.db', 'rb')
        await bot.send_document(message.chat.id, doc)
    conn.close()


@dp.message_handler(content_types=ContentTypes.PHOTO)
async def get_photo_id(message: types.Message,):
    await bot.send_message(message.chat.id, message.photo[-1])


if __name__ == '__main__':
    executor.start_polling(dp)