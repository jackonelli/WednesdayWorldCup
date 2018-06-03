"""Game module"""
import logging
from datetime import datetime
from lib.team import Team


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
        self.home_team = Team()
        self.away_team = Team()
        self.game_day = int()
        self.date = None
        self.home_result = '-'
        self.away_result = '-'

        self.finished = False

    def init_from_json(self, dict_, teams):
        self.id = dict_.name
        self.home_team = teams.get(dict_.home_team)
        self.away_team = teams.get(dict_.away_team)
        self.game_day = dict_.matchday
        self.date = datetime.strptime(''.join(dict_.date.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        self.home_result = dict_.home_result
        self.away_result = dict_.away_result
        self.finished = dict_.finished

    def print(self):
        string = str()
        if self.home_team and self.away_team:
            string = '{} - {}'.format(self.home_team.name, self.away_team.name)
        if self.finished:
            string += ': {} - {}'.format(self.home_result, self.away_result)
        string += ' ' + str(self.date)
        print(string)


class GroupGame(Game):
    """Game sub class for group play

    Attributes:
        group (Group): Group of game
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.group = str()

    def set_group(self, group):
        self.group = group


class PlayoffGame(Game):
    """Game sub class for playoff

    Attributes:
        self.home_parent (int, str): ID of previous game, the winner of which is home team
            If first round of playoff: str, e.g. 'winner_b' = The winner of group B
        self.away_parent (int, str): ID of previous game, the winner of which is away team
    """

    def __init__(self):
        super(self.__class__, self).__init__()
        self.order = int()
        self.home_team = None  # Override parent class
        self.away_team = None
        self.home_parent = None
        self.away_parent = None

    def init_from_json(self, dict_, teams):
        super(self.__class__, self).init_from_json(dict_, teams)
        self.home_parent = dict_.home_team
        self.away_parent = dict_.away_team

    def set_order(self, order):
        self.order = order

    def get_winner(self):
        """TODO raise error"""
        if self.home_result > self.away_result:
            winner = self.home_team
        elif self.home_result < self.away_result:
            winner = self.away_team
        else:
            winner = None
            self._log.error('No winner in playoff game id: {}'.format(self.id))

        return winner

    def get_loser(self):
        """TODO raise error"""
        if self.home_result > self.away_result:
            loser = self.away_team
        elif self.home_result < self.away_result:
            loser = self.home_team
        else:
            loser = None
            self._log.error('No winner in playoff game id: {}'.format(self.id))

        return loser
