import sqlite3
from aiogram import types


class GetUserData():
    def get_user_state(self):
        try:
            conn = sqlite3.connect('main.db')
            curs = conn.cursor()
            curs.execute('SELECT state FROM profiles WHERE id={}'.format(self.id))
            state = curs.fetchone()
            conn.close()
            return state
        except:
            return False

    def new_profile(self, username):
        print(self.id, username)
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('INSERT INTO profiles VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (int(self.id), username, 10, 10, 5, 5, 5, 'Лесное поселение', 0, 0, 1, 'normal'))
        curs.execute('SELECT * FROM profiles WHERE id={}'.format(self.id))
        print(curs.fetchone())
        conn.commit()
        curs.close()


    def get_user(self):
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT * FROM profiles WHERE id = {}'.format(self.id))
        user = curs.fetchone()
        conn.close()
        return user


    def get_location(self):
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT location FROM profiles WHERE id = {}'.format(self.id))
        location = curs.fetchone()
        conn.close()
        return location


    def get_buttons_by_location(self):
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT location FROM profiles WHERE id={}'.format(self.id))
        location = curs.fetchone()
        conn.close()
        if location[0] == 'Лесное поселение':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            btn1 = types.KeyboardButton('Профиль')
            btn2 = types.KeyboardButton('Локации')
            markup.add(btn1, btn2)
            return markup
        elif location[0] == 'Овраг':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton('Бой')
            btn2 = types.KeyboardButton('Профиль')
            btn3 = types.KeyboardButton('Локации')
            markup.add(btn1, btn2, btn3)
            return markup

    def __init__(self, id):
        self.id = id