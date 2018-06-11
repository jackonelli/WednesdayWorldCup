"""Score module"""
import logging
from abc import ABC, abstractmethod


class Score(ABC):
    """Score meta class"""

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def get_score(self, facit, player):
        pass

class SimpleScore(Score):
    """Simple score class"""

    def __init__(self, settings):
        """TODO: Description"""
        super(self.__class__, self).__init__()
        self.group_outcome = settings.group_outcome
        self.group_result = settings.group_result

        self.playoff_correct_game = settings.playoff.correct_game
        self.playoff_wrong_game = settings.playoff.wrong_game
        self.playoff.result = settings.playoff.result
        self.winner = settings.winner
        self.bronze = settings.bronze

        self.top_scorer = settings.top_scorer
        self.top_scorer_goal = settings.top_scorer_goal

    def get_score(self, facit, player):
        return 1
