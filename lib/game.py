"""Game module"""
import logging
from datetime import datetime


class Game(object):
    """Game class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        home_team (int): Home team ID
        away_team (int): Away team ID
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

    def print(self, teams):
        string = str()
        home_team = teams.get(self.home_team)
        away_team = teams.get(self.away_team)
        if home_team and away_team:
            home_team_name = home_team.name
            away_team_name = away_team.name
            string = '{} - {}'.format(home_team_name, away_team_name)
        if self.finished:
            string += ': {} - {}'.format(self.home_result, self.away_result)
        string += ' ' + str(self.date)
        print(string)


class GroupGame(Game):
    """Game sub class for group play

    Attributes:
        group (str): Group of game
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.group = str()

    def set_group(self, group_id):
        self.group = group_id


class PlayoffGame(Game):
    """Game sub class for playoff

    Attributes:
        self.home_parent (int, str): ID of previous game, the winner of which is home team
            If first round of playoff: str, e.g. 'winner_b' = The winner of group B
        self.away_parent (int, str): ID of previous game, the winner of which is away team
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.group = str()
        self.home_team = int()  # Override parent class
        self.away_team = int()
        self.home_parent = None
        self.away_parent = None

    def init_from_json(self, dict_):
        super(self.__class__, self).init_from_json(dict_)
        self.home_parent = dict_.home_team
        self.away_parent = dict_.away_team

    def set_order(self, order):
        self.group = order
