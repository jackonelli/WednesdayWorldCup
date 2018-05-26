"""Player module"""
import os
import random
import logging
from attrdict import AttrDict
from lib.score import Score
from util.io import read_json_to_attrdict


class Player(object):
    """Player class

    Attributes:
        _log (Logger)
        _settings (AttrDict): Meta settings
        name (str)
        predictions (dict): Flattened game dict game ID: game info.
        score (Score)
    """

    def __init__(self, settings, name):
        """Init Player

        Args:
            _settings (AttrDict): Meta settings
            name (str): Unique player name
        """
        self._log = logging.getLogger(self.__class__.__name__)
        self._settings = settings
        self.name = name
        self.predictions = list()
        self.score = Score()

    def generate_dummy_predictions(self, games):
        """ Generate random predictions for test"""
        for game_id, game in games.items():
            game.home_result = random.randint(0, 4)
            game.away_result = random.randint(0, 4)
        self.predictions = games

