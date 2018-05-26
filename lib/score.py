"""Score module"""
import logging


class Score:
    """Score class"""

    def __init__(self):
        self._log = logging.getLogger(self.__class__.__name__)
        self.score = 0
