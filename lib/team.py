"""Team module"""
import logging


class Team:
    """Team class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        name (str): Name of country
        iso2 (str): Iso2 code
        group (Group): Group affiliation
        points (int): Points in group play
        goals_diff (int): goal difference in group play
    """

    def __init__(self):
        """Init Team"""
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = int()
        self.name = str()
        self.fifa_code = str()
        self.iso2 = str()
        self.group = str()
        self.points = 0
        self.goals = 0
        self.goal_diff = 0

    def __repr__(self):
        """Representation

        Returns:
            string (str): Team representation
        """

        string = 'Team(id: {}, name (fifa code): {} ({}), points: {}, '.format(self.id, self.name,
                                                                               self.fifa_code,
                                                                               self.points)
        return string

    def __str__(self):
        """To string

        Returns:
            string (str): Team to string
        """

        return '{} ({})'.format(self.name, self.fifa_code)

    def init_from_json(self, dict_):
        """Init from github sourced JSON file

        Args:
            dict_ (dict): Dictionary version of JSON data
        """

        self.id = dict_.id
        self.name = dict_.name
        self.fifa_code = dict_.fifaCode
        self.iso2 = dict_.iso2

    def set_group(self, group):
        """Add group affiliation

        Args:
            group (Group)
        """
        self.group = group
