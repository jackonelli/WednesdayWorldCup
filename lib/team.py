"""Team module"""
import logging


class Team:
    """Team class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        name (str): Name of country
        iso2 (str): Iso2 code
        group (str): Group ID ('Group A', ..., 'Group H')
        points (int): Points in group play
        goals_scored (int): goals scored in group play
        goals_conceded (int): goals conceded in group play
    """

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = int()
        self.name = str()
        self.fifa_code = str()
        self.iso2 = str()
        self.group = str()
        self.points = 0
        self.goals = 0
        self.goal_diff = 0

    def init_from_json(self, dict_):
        self.id = dict_.id
        self.name = dict_.name
        self.fifa_code = dict_.fifaCode
        self.iso2 = dict_.iso2

    def set_group(self, group):
        self.group = group
