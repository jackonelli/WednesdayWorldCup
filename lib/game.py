"""Game module"""
import logging
from datetime import datetime
from lib.team import Team


class Game(object):
    """Game class

    Attributes:
        _log (Logger): Logger
        id (int): Unique key
        home_team (Team): Home team ID
        away_team (Team): Away team ID
        game_day (int):
        date (datetime):
        home_result (int): Goals scored by home team
        away_result (int): Goals scored by away team
        finished (bool): Played indicator
    """

    def __init__(self):
        """Init Game"""
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = int()
        self.home_team = Team()
        self.away_team = Team()
        self.game_day = int()
        self.date = None
        self.home_result = None
        self.away_result = None

        self.finished = False

    def __repr__(self):
        """Representation

        Returns:
            string (str): Game representation
        """

        string = 'Game(id: {}, home team_id (score): {} ({}), away team_id (score): {} ({}), date: {})'.format(
            self.id, self.home_team.id, self.home_result, self.away_team.id, self.away_result, self.date)
        return string

    def __str__(self):
        """To string

        Returns:
            string (str): Game to string
        """

        if self.home_team and self.away_team:
            string = '{} - {}'.format(self.home_team.name, self.away_team.name)
        if self.finished:
            string += ': {} - {}'.format(self.home_result, self.away_result)
        string += ' ' + str(self.date)
        return string

    def init_from_json(self, dict_, teams):
        """Init from github sourced JSON file

        Args:
            dict_ (dict): Dictionary version of JSON data
            teams (AttrDict): Dictionary of Team()s
        """

        self.id = dict_.name
        self.home_team = teams.get(dict_.home_team)
        self.away_team = teams.get(dict_.away_team)
        self.game_day = dict_.matchday
        self.date = datetime.strptime(''.join(dict_.date.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        self.home_result = dict_.home_result
        self.away_result = dict_.away_result
        self.finished = dict_.finished


class GroupGame(Game):
    """Game sub class for group play

    Attributes:
        group (Group): Group of game
    """

    def __init__(self):
        """Init group game"""
        super(self.__class__, self).__init__()
        self.group = str()

    def set_group(self, group):
        """Add group affiliation

        Args:
            group (Group)
        """
        self.group = group

    def evaluate(self):
        """Evaluate a group game

        Determine winner, assign points, update goal difference.
        TODO: Better failed result handling
        """

        home_team = self.home_team
        away_team = self.away_team
        if self.home_result > self.away_result:
            home_team.points += 3
        elif self.home_result == self.away_result:
            home_team.points += 1
            away_team.points += 1
        elif self.home_result < self.away_result:
            away_team.points += 3
        else:
            self._log.error('Failed result comparison in game: {}'.format(self.id))
        home_team.goal_diff += self.home_result - self.away_result
        away_team.goal_diff += self.away_result - self.home_result
        home_team.games_played += 1
        away_team.games_played += 1


class PlayoffGame(Game):
    """Game sub class for playoff

    Attributes:
        order (int): Power of two, showing final distance. (Number of teams in round)
        self.home_team (Team)
        self.away_team (Team)
        self.home_parent (int, str): ID of previous game, the winner of which is home team
            If first round of playoff: str, e.g. 'winner_b' = The winner of group B
        self.away_parent (int, str): ID of previous game, the winner of which is away team
    """

    def __init__(self):
        """Init playoff game"""
        super(self.__class__, self).__init__()
        self.order = int()
        self.home_team = None  # Override parent class
        self.away_team = None
        self.home_parent = None
        self.away_parent = None

    def init_from_json(self, dict_, teams):
        """Init from github sourced JSON file

        Args:
            dict_ (dict): Dictionary version of JSON data
            teams (AttrDict): Dictionary of Team()s
        """

        super(self.__class__, self).init_from_json(dict_, teams)
        self.home_parent = dict_.home_team
        self.away_parent = dict_.away_team

    def set_order(self, order):
        """Set order

        Args:
            order (int):

        """
        self.order = order

    def get_winner(self):
        """Get winner of TODO raise error"""
        if self.home_result > self.away_result:
            winner = self.home_team
        elif self.home_result < self.away_result:
            winner = self.away_team
        else:
            winner = None
            self._log.error('No winner in playoff game id: {}'.format(self.id))

        return winner

    def get_loser(self):
        """Get winner of TODO raise error"""
        if self.home_result > self.away_result:
            loser = self.away_team
        elif self.home_result < self.away_result:
            loser = self.home_team
        else:
            loser = None
            self._log.error('No winner in playoff game id: {}'.format(self.id))

        return loser
