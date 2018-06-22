from collections import defaultdict
from dicttoxml import dicttoxml as dtx
import pickle

def save(save_obj, file_name):
    """Сохранение объекта в файл"""
    with open(file_name, 'wb') as file:
        pickle.dump(save_obj, file)
    print("File is saved to disk")

def load(file_name):
    import os.path
    load_obj = str()
    """Чтение статистики из файла"""
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as f:
            load_obj = pickle.load(f)
        print('OK')
        return load_obj
    else:
        print('Statistic file not exist' % file_name)

class Group(object):
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.group_stats = []

    def __repr__(self):
        return 'Group \'%s\' (%i)' % (self.name, len(self.teams))

    def __str__(self):
        if not self.teams:
            return 'Group \'%s\' is empty' % self.name
        else:
            return self.group_table()

    def __add__(self, other):
        if isinstance(other, Group):
            new = Group('All')
            new.group_stats = defaultdict(dict)
            new.teams.extend(self.teams)
            new.teams.extend(other.teams)
            for key,value in self.group_stats.items():
                new.group_stats[key] = value
            for key,value in other.group_stats.items():
                new.group_stats[key] = value
            return new

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

    def add_game_result(self, team1, team2, game_score):
        """Добаление результата матча в статистику"""
        t1 = self.teams.index(team1)
        t2 = self.teams.index(team2)
        self.group_stats[self.teams[t1]][self.teams[t2]] = game_score
        self.group_stats[self.teams[t2]][self.teams[t1]] = game_score[::-1]
        self.__add_game_stats(self.teams[t1],self.teams[t2], score=game_score)

    def sort_list(self):
        """Сортировка комманд группы по убыванию (сначала по очкам, потом по разнице мячей)"""
        list = [(k, v['pts'], v['gf_a']) for k,v in self.group_stats.items()]
        sort_list = sorted(list, key=lambda point: (-point[1], -point[2]))
        return sort_list

    def group_table(self):
        """Вывод таблицы группы на экран"""
        s = str()
        if self.teams:
            list = self.sort_list()
            s += 'Group %s\n' % self.name
            s += '\t\t\t\tWins\tDraws\tLoses\tGF\tGA\t+\-\tPts\n'
            for items in list:
                item = items[0]
                if len(item.split()) > 2:
                    name = '%s' % item
                elif len(item.split()) > 1:
                    name = '%s\t' % item
                elif len(item.split()) == 1 and len(item) > 7:
                    name = '%s\t' % item
                else:
                    name = '%s\t\t' % item
                s += '\t%s\t%i\t%i\t%i\t%i\t%i\t%i\t%i\n' % (name, self.group_stats[item]['w'],
                        self.group_stats[item]['d'], self.group_stats[item]['l'], self.group_stats[item]['gf'],
                        self.group_stats[item]['ga'], self.group_stats[item]['gf_a'], self.group_stats[item]['pts'])
            return s
        else:
            print(self)

    def save_to_file(self):
        """ Сохранение статистики комманд в файл """
        file_name = self.name + '.group'
        save(self.group_stats, file_name)

    def load_from_file(self):
        """ Чтение статистики команд из файла """
        file_name = self.name + '.group'
        self.group_stats = load(file_name)
        self.teams = [s for s in self.group_stats.keys() if isinstance(s, str)]

class Tournament(object):
    """ Класс турнир """
    def __init__(self,name):
        self.name = name
        self.__groups = []

    def add_groups(self, num):
        """ Метод для создания нужного количества групп турнира """
        groups = []
        for i in range(num):
            groups.append(Group(chr(i + 65)))
            print(groups[i])
        self.__groups = groups

    def __repr__(self):
        return self.name

    def __str__(self):
        if not self.__groups:
            return 'Tournament \'%s\' is not initialized' % self.name
        else:
            for i in self.__groups:
                print(i)
            return str()

    def __group_num(self, group):
        """ Метод для получения номера группы по ее букве"""
        return ord(group) - 65

    def add_game_result(self, group, *teams, score):
        """ Метод для добавления результата матча турнира в группу
            все параметры строковые!
            первый: буква группы (заглавная)
            второй и третий: комманды через запятую,
            последний: счет """
        group_num = self.__group_num(group)
        self.__groups[group_num].add_game_result(*teams, game_score=score)

    def add_teams(self, group, *teams):
        """ Метод для добавления команд турнира в группу
            все параметры строковые!
            первый: буква группы (заглавная)
            второй и третий: комманды через запятую """
        group_num = self.__group_num(group)
        self.__groups[group_num].add_teams(*teams)

    def save_to_file(self, name):
        """Сохранение статистики турнира в файл"""
        file_name = name + '.tour'
        save(self.__groups, file_name)

    def load_from_file(self, name):
        """Чтение статистики турнира из файла"""
        file_name = name + '.tour'
        self.__groups = load(file_name)

