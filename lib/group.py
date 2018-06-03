"""Group module"""
import logging


class Group:
    """Group class

    Attributes:
        _log (Logger): Logger
        id (str): Unique key
        name (): Group name
        teams (list): Team ID's
        winner (int): Winning team ID, None if group not finished
        runner_up (int): Runner up team ID, None if group not finished
        games (list): GroupGame ID's
        finished (bool): All matches played
    """

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = str()
        self.name = str()
        self.teams = list()
        self.winner = int()
        self.runner_up = int()
        self.games = list()
        self.finished = False

    def init_from_json(self, dict_, prefix):
        """TODO: Validate self.id better"""
        self.id = dict_.name[-1]
        self.name = prefix + self.id

    def add_game(self, game):
        """TODO: Validate game"""
        self.games.append(game)

    def add_teams(self, home, away):
        ids = [team.id for team in self.teams]
        if home.id not in ids:
            self.teams.append(home)
        if away.id not in ids:
            self.teams.append(away)

    def set_group_status(self):
        self.finished = True
        for game in self.games:
            self.finished = self.finished and game.finished

    def sort(self):
        self.teams.sort(key=lambda team: team.points, reverse=True)
        self.games.sort(key=lambda game: game.date)

        #game_dates = [games[id_].date for id_ in self.games]
        #self.games = [game for _, game in sorted(zip(game_dates, self.games),
        #                                         key=lambda pair: pair[0])]

    def evaluate(self):
        for game in self.games:
            if game.finished:
                home_team = game.home_team
                away_team = game.away_team
                if game.home_result > game.away_result:
                    home_team.points += 3
                elif game.home_result == game.away_result:
                    home_team.points += 1
                    away_team.points += 1
                elif game.home_result < game.away_result:
                    away_team.points += 3
                else:
                    self._log.error('Failed result comparison in game: {}'.format(game.id))
                home_team.goals += game.home_result
                home_team.goal_diff += game.home_result - game.away_result
                away_team.goals += game.away_result
                away_team.goal_diff += game.away_result - game.home_result
        self.sort()

    def set_winner_and_loser(self):
        self.set_group_status()
        self.sort()
        if self.finished:
            self.winner = self.teams[0]
            self.runner_up = self.teams[1]

    def print(self):
        print(self.name)
        print('-------')
        for team in self.teams:
            team.print()

