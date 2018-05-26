"""Team module"""
import logging


class Team:
    """Team class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        name (str): Name of country
        group (str): Group ID ('Group A', ..., 'Group H')
        points (int): Points in group play
        goals_scored (int): goals scored in group play
        goals_conceded (int): goals conceded in group play
    """

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = int()
        self.name = str()
        self.group = str()
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0

    def init_from_json(self, dict_):
        self.id = dict_.id
        self.name = dict_.name

    def set_group(self, group):
        self.group = group
