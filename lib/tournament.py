"""Tournament module"""
import os
import logging
from attrdict import AttrDict
import urllib.request
from util.io import read_json_to_attrdict
from lib.team import Team
from lib.group import Group
from lib.game import Game


class Tournament(object):
    """Tournament class

    Attributes:
        _log (Logger): Logger
        _settings (AttrDict): Meta settings
        teams (dict): Dict of all Teams
        groups (dict): Dict of all Groups
        games (dict): Dict of all Games
        playoff: TODO
    """

    def __init__(self, settings):
        """Initialise tournament

        Args:
            settings (AttrDict): General settings
        """
        self._log = logging.getLogger(self.__class__.__name__)
        self._settings = settings
        self.teams = dict()
        self.groups = dict()
        self.games = dict()
        self.playoff = None  # TODO: handle

        # In case of JSON file from Github
        if settings.data.src == 'github':
            self.url = settings.data.url
            self.data_root = os.path.join(self._settings.root, self._settings.data.dir)
            self.data_file = 'data' + self._settings.data.extension
        else:
            self._log.error('No other source than Github found yet')

    def populate(self):
        """Set current tournament state."""
        src = self._settings.data.src
        self._update_data(src)
        if src == 'github':
            self._populate_from_json()
        else:
            self._log.error('No other source than Github found yet')

    def _update_data(self, src):
        if src == 'github':
            urllib.request.urlretrieve(self.url, os.path.join(self.data_root, self.data_file))
        else:
            self._log.error('No other source than Github found yet')

    def _populate_from_json(self):
        """Ugly match up to force the Github JSON data to the class structure"""
        data_dict = read_json_to_attrdict(os.path.join(self.data_root, self.data_file))
        for team_data in data_dict.teams:
            team = Team()
            team.init_from_json(team_data)
            self.teams[team.id] = team

        for group_id in data_dict.groups:
            group_data = AttrDict(data_dict.groups[group_id])
            group = Group()
            group.init_from_json(group_data)
            for game_data in group_data.matches:
                group.add_game_id(game_data.name)
                group.add_teams(game_data.home_team, game_data.away_team)

                game = Game()
                game.init_from_json(game_data)
                game.set_type(group.id)
                self.games[game.id] = game
            self.groups[group.id] = group

    def print_groups(self):
        for _, group in sorted(self.groups.items()):
            group.print(self.teams)
            print('\n')

    def print_games(self):
        prev_game_day = -1
        for game_id in sorted(self.games, key=lambda id_: self.games[id_].game_day):
            game = self.games[game_id]
            if game.game_day == prev_game_day:
                game.print(self.teams)
            else:
                print('\nDay: {}\t {}\n'.format(game.game_day, game.date))
                game.print(self.teams)
            prev_game_day = game.game_day
