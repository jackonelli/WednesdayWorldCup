"""Group module"""
import logging
from lib.game import GroupGame


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
        """Init Group"""
        self._log = logging.getLogger(self.__class__.__name__)
        self.id = str()
        self.name = str()
        self.teams = list()
        self.winner = int()
        self.runner_up = int()
        self.games = list()
        self.finished = False

    def __repr__(self):
        """Representation

        Returns:
            string (str): Group representation
        """

        string = 'Group(id: {}, name: {}, finished: {}, '.format(self.id, self.name, self.finished)
        if self.winner:
            string += 'winner id: {}, '.format(self.winner.id)
        if self.runner_up:
            string += 'runner up id: {}, '.format(self.runner_up.id)
        return string

    def __str__(self):
        """To string

        Returns:
            string (str): Group to string
        """

        string = '{}: '.format(self.name)
        for team in self.teams:
            string += '{}, '.format(team.__str__())
        return string

    def init_from_json(self, dict_, prefix):
        """Init from github sourced JSON file

        TODO: Validate self.id better

        Args:
            dict_ (dict): Dictionary version of JSON data
            prefix (str): First part of group name, e.g. 'GROUP '
        """
        self.id = dict_.name[-1]
        self.name = prefix + self.id

    def add_game(self, game):
        """Add group game to group

        Args:
            game (GroupGame)
        """

        if isinstance(game, GroupGame):
            self.games.append(game)
        else:
            self._log.error('Not a group game, game: {}'.format(game.__str__))

    def add_teams(self, home, away):
        """Add teams to group

        Checks if home and or away is missing from team list, and if so adds them

        Args:
            home (Team)
            away (Team)
        """

        ids = [team.id for team in self.teams]
        if home.id not in ids:
            self.teams.append(home)
        if away.id not in ids:
            self.teams.append(away)

    def set_group_status(self):
        """Set group status"""
        self.finished = True
        for game in self.games:
            self.finished = self.finished and game.finished

    def sort(self):
        """Sort group

        TODO: Sort group on points --> diff --> inbordes games
        """

        self.teams.sort(key=lambda team: team.points, reverse=True)
        self.games.sort(key=lambda game: game.date)

    def evaluate(self):
        """Evaluate group as far as possible

        Assigns points to teams
        """

        for game in self.games:
            if game.finished:
                game.evaluate()
        self.sort()
        self.set_winner_and_runner_up()

    def set_winner_and_runner_up(self):
        """Update group with winner and runner up"""
        self.set_group_status()
        if self.finished:
            self.winner = self.teams[0]
            self.runner_up = self.teams[1]

    def get_game_from_teams(self, team_a, team_b):
        """For inbordes game comparison

        Returns:
            correct_game (GroupGame):
        """
        id_a = team_a.id
        id_b = team_b.id
        a_games = list()
        correct_game = None
        for game in self.games:
            if game.home_team.id == id_a or game.away_team.id == id_a:
                a_games.append(game)
        for game in a_games:
            if game.home_team.id == id_b or game.away_team.id == id_b:
                correct_game = game

        if not correct_game:
            self._log.error('No game with teams {} and {} in {}'.format(team_a.__str__,
                                                                        team_b.__str__,
                                                                        self.__str__))
        return correct_game
