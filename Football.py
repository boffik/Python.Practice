from collections import defaultdict

class Group:
    teams = []
    games = []
    def __init__(self, name):
        self.name = name

    def __make_array(self):
        new_games = defaultdict(dict)
        for i in range(len(self.teams)):
            for j in range(i, len(self.teams) - 1):
                new_games[self.teams[i]][self.teams[j + 1]] = None
                new_games[self.teams[j + 1]][self.teams[i]] = None
                self.__add_def_stats((self.teams[i], self.teams[j + 1]), new_games)
        self.games = new_games

    def __add_def_stats(self, list, dict):
        for item in list:
            dict[item]['pts'] = 0
            dict[item]['gf'] = 0
            dict[item]['ga'] = 0
            dict[item]['gf_a'] = 0
            dict[item]['w'] = 0
            dict[item]['d'] = 0
            dict[item]['l'] = 0

    def __add_game_stats(self, list, score):
        i = 0
        dict = self.games
        goals = [int(s) for s in score.split(':')]
        for item in list:
            if i == 0:
                if goals[0] > goals[1]:
                    dict[item]['pts'] += 3
                    dict[item]['w'] += 1
                elif goals[0] < goals[1]:
                    dict[item]['l'] += 1
                else:
                    dict[item]['pts'] += 1
                    dict[item]['d'] += 1

                dict[item]['gf'] += goals[0]
                dict[item]['ga'] += goals[1]
                dict[item]['gf_a'] += (goals[0] - goals[1])
                i += 1
            else:
                if goals[0] < goals[1]:
                    dict[item]['pts'] += 3
                    dict[item]['w'] += 1
                elif goals[0] > goals[1]:
                    dict[item]['l'] += 1
                else:
                    dict[item]['pts'] += 1
                    dict[item]['d'] += 1

                dict[item]['gf'] += goals[1]
                dict[item]['ga'] += goals[0]
                dict[item]['gf_a'] += (goals[1] - goals[0])

    def add_team(self, team):
        if team not in self.teams:
            self.teams.append(team)
        else:
            print('Team \'%s\' already in group \'%s\'' % (team, self.name))
        if len(self.teams) > 1:
            self.__make_array()

    def print_teams(self):
        if len(self.teams) > 0:
            for team in self.teams:
                print(team)
        else:
            print('Group \'%s\' is empty' % self.name)

    def add_game_result(self, team1, team2, score):
        t1 = self.teams.index(team1)
        t2 = self.teams.index(team2)
        self.games[self.teams[t1]][self.teams[t2]] = score
        self.games[self.teams[t2]][self.teams[t1]] = score[::-1]
        self.__add_game_stats((self.teams[t1],self.teams[t2]), score)

    def sort_list(self):
        list = [(k, v['pts'], v['gf_a']) for k,v in self.games.items()]
        sort_list = sorted(list, key=lambda point: (-point[1], -point[2]))
        return sort_list

    def group_table(self):
        list = self.sort_list()
        print('Group %s' % self.name)
        print('\t\t\t\tWins\tDraws\tLoses\tGF\tGA\t+\-\tPts')
        for items in list:
            item = items[0]
            if len(item.split()) > 1:
                name = '%s\t' % item
            else:
                name = '%s\t\t' % item
            print('\t%s\t%i\t%i\t%i\t%i\t%i\t%i\t%i' % (name, self.games[item]['w'],
                    self.games[item]['d'], self.games[item]['l'], self.games[item]['gf'],
                    self.games[item]['ga'], self.games[item]['gf_a'], self.games[item]['pts']))
