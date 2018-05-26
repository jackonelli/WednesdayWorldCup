"""Group module"""
import logging


class Group:
    """Group class

    Attributes:
        _log (Logger): Logger
        id (str): Unique key
        teams (list): Team ID's
        winner (int): Winning team ID, None if group not finished
        runner_up (int): Runner up team ID, None if group not finished
        games (list): Game ID's
        finished (bool): All matches played
    """

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = str()
        self.teams = list()
        self.winner = None
        self.runner_up = int()
        self.games = list()
        self.finished = False

    def init_from_json(self, dict_):
        self.id = dict_.name

    def add_game_id(self, game_id):
        self.games.append(game_id)

    def add_teams(self, home, away):
        game_teams = [home, away]
        self.teams = list(set(self.teams + game_teams))  # Add new teams to group

    def print(self, teams):
        print(self.id)
        print('-------')
        for team_id in self.teams:
            print(teams[team_id].name)

