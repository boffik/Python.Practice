from collections import defaultdict
from dicttoxml import dicttoxml as dtx

class Group:
    teams = []
    group_stats = []

    def __init__(self, name):
        self.name = name

    def __make_array(self):
        """Создаем словарь согласно списка команд в группе и заполняем статистикой по дефолту"""
        new_stats = defaultdict(dict)
        for i in range(len(self.teams)):
            for j in range(i, len(self.teams) - 1):
                new_stats[self.teams[i]][self.teams[j + 1]] = None
                new_stats[self.teams[j + 1]][self.teams[i]] = None
                self.__add_def_stats((self.teams[i], self.teams[j + 1]), new_stats)
        self.group_stats = new_stats

    def __add_def_stats(self, list, dict):
        """Заполнение каждого элемента списка дефолтной статистикой"""
        for item in list:
            dict[item]['pts'] = 0
            dict[item]['gf'] = 0
            dict[item]['ga'] = 0
            dict[item]['gf_a'] = 0
            dict[item]['w'] = 0
            dict[item]['d'] = 0
            dict[item]['l'] = 0

    def __add_game_stats(self, *team, score):
        """Заполнение статистики матча двух комманд согласно итогового счета игры"""
        dict = self.group_stats
        goals = [int(s) for s in score.split(':')]
        if goals[0] > goals[1]:
            dict[team[0]]['pts'] += 3
            dict[team[0]]['w'] += 1
            dict[team[1]]['l'] += 1
        elif goals[0] < goals[1]:
            dict[team[1]]['pts'] += 3
            dict[team[1]]['w'] += 1
            dict[team[0]]['l'] += 1
        else:
            dict[team[0]]['pts'] += 1
            dict[team[0]]['d'] += 1
            dict[team[1]]['pts'] += 1
            dict[team[1]]['d'] += 1

        dict[team[0]]['gf'] += goals[0]
        dict[team[0]]['ga'] += goals[1]
        dict[team[0]]['gf_a'] += (goals[0] - goals[1])
        dict[team[1]]['gf'] += goals[1]
        dict[team[1]]['ga'] += goals[0]
        dict[team[1]]['gf_a'] += (goals[1] - goals[0])

    def add_teams(self, *teams):
        """Добавление списка комманд в группу и заполнение дефолтной статистикой"""
        for team in teams:
            if team not in self.teams:
                self.teams.append(team)

        if len(self.teams) > 1:
            self.__make_array()


    def print_teams(self):
        if len(self.teams) > 0:
            for team in self.teams:
                print(team)
        else:
            print('Group \'%s\' is empty' % self.name)

    def add_game_result(self, team1, team2, game_score):
        """Добаление результата матча в статистику"""
        t1 = self.teams.index(team1)
        t2 = self.teams.index(team2)
        self.group_stats[self.teams[t1]][self.teams[t2]] = game_score
        self.group_stats[self.teams[t2]][self.teams[t1]] = game_score[::-1]
        self.__add_game_stats(self.teams[t1],self.teams[t2], score=game_score)

    def sort_list(self):
        """Сортировка комманд группы по убыванию (сначала по очкам, потом по разнице мячей"""
        list = [(k, v['pts'], v['gf_a']) for k,v in self.group_stats.items()]
        sort_list = sorted(list, key=lambda point: (-point[1], -point[2]))
        return sort_list

    def group_table(self):
        """Вывод таблицы группы на экран"""
        list = self.sort_list()
        print('Group %s' % self.name)
        print('\t\t\t\tWins\tDraws\tLoses\tGF\tGA\t+\-\tPts')
        for items in list:
            item = items[0]
            if len(item.split()) > 2:
                name = '%s' % item
            elif len(item.split()) > 1:
                name = '%s\t' % item
            else:
                name = '%s\t\t' % item
            print('\t%s\t%i\t%i\t%i\t%i\t%i\t%i\t%i' % (name, self.group_stats[item]['w'],
                    self.group_stats[item]['d'], self.group_stats[item]['l'], self.group_stats[item]['gf'],
                    self.group_stats[item]['ga'], self.group_stats[item]['gf_a'], self.group_stats[item]['pts']))

    def save_xml(self):
        """Сохранение статистики комманд в файл XML"""
        xml = dtx(self.group_stats, custom_root=self.name, attr_type=False)
        with open(self.name + '.xml', 'w') as file:
            file.write(xml.decode('utf-8'))
        print("File is saved to disk")
