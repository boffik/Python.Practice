import random

"""
В основной ветке программы создается по одному герою для каждой команды. 
В цикле генерируются объекты-солдаты. Их принадлежность команде определяется случайно. 
Солдаты разных команд добавляются в разные списки.
Измеряется длина списков солдат противоборствующих команд и выводится на экран. 
У героя, принадлежащего команде с более длинным списком, поднимается уровень (в случае равенства - обоим).
Отправьте одного из солдат первого героя следовать за ним. 
Выведите на экран идентификационные номера этих двух юнитов.
"""

class Member:
    id = int()
    group = str()

    def __init__(self, id, group):
        self.id = id
        self.group = group

class Hero(Member):
    level = int()

    def __init__(self,id, group, level=0):
        Member.__init__(self, id, group)
        self.level = level

    def up_level(self):
        self.level += 1

class Solder(Member):
    hero = ""

    def GoFromHero(self, Hero):
        self.hero = Hero


if __name__ == '__main__':
    commands = ('Black', 'White')
    hero_black = Hero(1, commands[0])
    hero_white = Hero(2, commands[1])

    solders_black = []
    solders_white = []
    for i in range(10):
        solder = Solder(i + 3, commands[random.randrange(0,2)])
        if solder.group == "Black":
            solders_black.append(solder)
        else:
            solders_white.append(solder)
    len_black = len(solders_black)
    len_white = len(solders_white)
    s_items_black = (' '.join([str(solderb.id) for solderb in solders_black]))
    s_items_white = (' '.join([str(solderw.id) for solderw in solders_white]))
    print('Count of solders in Black [%s] : %i' % (s_items_black, len_black))
    print('Count of solders in White [%s] : %i' % (s_items_white, len_white))

    if len_black > len_white:
        hero_black.up_level()
    elif len_black < len_white:
        hero_white.up_level()
    else:
        hero_white.up_level()
        hero_black.up_level()

    print("The level of Hero the first group: %i \nThe level of Hero the second group: %i" % (hero_black.level, hero_white.level))

    rnd_solder_black = random.choice(solders_black)
    rnd_solder_black.GoFromHero(hero_black)
    print('Solder %i went after the Hero %i' % (rnd_solder_black.id, rnd_solder_black.hero.id))
