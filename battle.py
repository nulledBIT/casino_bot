import random
import sqlite3


def crit_calculation(luck):
    crit_koef = random.randint(0, 100)
    if crit_koef < (int(luck) + 1):
        crit = True
    else:
        crit = False
    return crit


def evade_calculation(agilty):
    evade_koef = random.randint(1, 100)
    if evade_koef < (int(agilty) + 1):
        evade = True
    else:
        evade = False
    return evade

class Battle():
    def get_user_battle_data(self):
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT id, name, hp, str, def, luck, agilty FROM profiles WHERE id={}'.format(self.user_id))
        user = curs.fetchone()
        Battle.user_name = user[1]
        Battle.user_hp = user[2]
        Battle.user_str = user[3]
        Battle.user_def = user[4]
        Battle.user_luck = user[5]
        Battle.user_agilty = user[6]
        conn.close()

    def get_mob_battle_data(self):
        conn = sqlite3.connect('main.db')
        curs = conn.cursor()
        curs.execute('SELECT id, name, hp, str, def, luck, agilty FROM mobs WHERE id={}'.format(self.mob_id))
        mob = curs.fetchone()
        Battle.mob_name = mob[1]
        Battle.mob_hp = mob[2]
        Battle.mob_str = mob[3]
        Battle.mob_def = mob[4]
        Battle.mob_luck = mob[5]
        Battle.mob_agilty = mob[6]
        conn.close()

    def fight(self):
        user_impact = ['вмазал со всей дури', 'оступился и врезался в моба', 'оскорбил маму', 'нанес удар']
        mob_impact = ['раскинув тентакли сделал непроятно', 'искупал тебя в слизи', 'обнял как брата', 'сел на тебя']
        logs = 'Начало боя\nХп игрока: ❤{0}, хп моба: ❤{1}\n'.format(Battle.user_hp, Battle.mob_hp)
        turn = random.randint(0, 1)
        while Battle.user_hp > 0 and Battle.mob_hp > 0:
            if turn == 1:
                Battle.mob_evade = not evade_calculation(Battle.mob_agilty)
                Battle.crit = crit_calculation(Battle.user_luck)

                if Battle.mob_evade:
                    if Battle.crit:
                        Battle.mob_hp = Battle.mob_hp - (Battle.user_str * 1.5) * (1 - Battle.mob_def / 100)
                        logs += 'Игрок критично {1} ⚡{0}\n'.format(round((Battle.user_str * 1.5) * (1 - Battle.mob_def / 100), 2), random.choice(user_impact))
                    else:
                        Battle.mob_hp = Battle.mob_hp - (Battle.user_str) * (1 - Battle.mob_def / 100)
                        logs += 'Игрок {1} 💥{0}\n'.format(round((Battle.user_str) * (1 - Battle.mob_def / 100), 2), random.choice(user_impact))
                else:
                    logs += '💨Моб избежал атаки игрока\n'
                turn -= 1
            elif turn == 0:
                Battle.evade = not evade_calculation(Battle.user_agilty)
                Battle.mob_crit = crit_calculation(Battle.mob_luck)

                if Battle.evade:
                    if Battle.mob_crit:
                        Battle.user_hp = Battle.user_hp - (Battle.mob_str * 1.5) * (1 - Battle.user_def / 100)
                        logs += 'Моб с особым цинизмом {1} ⚡{0}\n'.format(round((Battle.mob_str * 1.5) * (1 - Battle.user_def / 100), 2), random.choice(mob_impact))
                    else:
                        Battle.user_hp = Battle.user_hp - (Battle.mob_str) * (1 - Battle.user_def / 100)
                        logs += 'Моб {1} 💥{0}\n'.format(round((Battle.mob_str) * (1 - Battle.user_def / 100), 2), random.choice(mob_impact))
                else:
                    logs += '💨Игрок избежал удара моба\n'
                turn += 1

        if Battle.user_hp > Battle.mob_hp:
            logs += 'Бой завершен\nХп игрока: ❤{0}🎉, хп моба: ❤{1}💀\nИгрок побдил'.format(round(Battle.user_hp, 2), round(Battle.mob_hp, 2))
        else:
            logs += 'Бой завершен\nХп игрока: ❤{0}💀, хп моба: ❤{1}🎉\nМоб побдил'.format(round(Battle.user_hp, 2), round(Battle.mob_hp, 2))
        return logs

    def __init__(self, user_id, mob_id):
        self.user_id = user_id
        self.mob_id = mob_id
