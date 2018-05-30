"""Game module"""
import logging
from datetime import datetime


class Game:
    """Game class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        home_team (int): Home team ID
        away_team (int): Away team ID
        type (str): Game type ('Group A', ..., 'Group H', 'round_16', ..., 'round_2')
        game_day (int):
        date (datetime):
        home_result (int): Goals scored by home team
        away_result (int): Goals scored by away team
        finished (bool): Played indicator
    """

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = int()
        self.home_team = int()
        self.away_team = int()
        self.type = str()
        self.game_day = int()
        self.date = None
        self.home_result = '-'
        self.away_result = '-'

        self.finished = False

    def init_from_json(self, dict_):
        self.id = dict_.name
        self.home_team = dict_.home_team
        self.away_team = dict_.away_team
        self.game_day = dict_.matchday
        self.date = datetime.strptime(''.join(dict_.date.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        self.home_result = dict_.home_result
        self.away_result = dict_.away_result
        self.finished = dict_.finished

    def set_type(self, type):
        self.type = type

    def print(self, teams):
        home_team = teams[self.home_team].name
        away_team = teams[self.away_team].name
        string = '{} - {}'.format(home_team, away_team)
        if self.finished:
            string += ': {} - {}'.format(self.home_result, self.away_result)
        print(string)
