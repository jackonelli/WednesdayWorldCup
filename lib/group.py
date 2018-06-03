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

    def add_game_id(self, game_id):
        self.games.append(game_id)

    def add_teams(self, home, away):
        game_teams = [home, away]
        self.teams = list(set(self.teams + game_teams))  # Add new teams to group

    def set_group_status(self, games):
        self.finished = True
        for game_id in self.games:
            game = games[game_id]
            self.finished = self.finished and game.finished

    def sort(self, teams, games):
        team_points = [teams[id_].points for id_ in self.teams]
        self.teams = [team_id for _, team_id in sorted(zip(team_points, self.teams),
                                                       key=lambda pair: pair[0], reverse=True)]

        game_dates = [games[id_].date for id_ in self.games]
        self.games = [game for _, game in sorted(zip(game_dates, self.games),
                                                 key=lambda pair: pair[0])]

    def evaluate(self, games, teams):
        for game_id in self.games:
            game = games[game_id]
            if game.finished:
                home_team = teams[game.home_team]
                away_team = teams[game.away_team]
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
        self.sort(teams, games)

    def print(self, teams):
        print(self.id)
        print('-------')
        for team_id in self.teams:
            teams[team_id].print()

