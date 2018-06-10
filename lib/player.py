"""Player module"""
import os
import random
import logging
from attrdict import AttrDict
from lib.score import Score
from util.io import read_xls_to_class
from util.io import read_json_to_attrdict
from util.io import write_dict_to_json


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
        self.predictions = dict()
        self.score = Score()

    def predictions_from_json(self):
        """Game predictions from JSON file.

        File at data_dir/predictions/name.json

        File written by self.epa_data_from_xls
        """
        root = self._settings.root
        json_file = os.path.join(root, self._settings.data.dir, 'predictions',
                                 self.name + '.json')

        dict_ = read_json_to_attrdict(json_file)
        self.predictions = {int(key): AttrDict(value) for key, value in dict_.items()}

    def generate_dummy_predictions(self, games):
        """ Generate random predictions for test"""
        for game_id, game in games.items():
            game.home_result = random.randint(0, 4)
            game.away_result = random.randint(0, 4)
        self.predictions = games

    def epa_data_from_xls(self, game_ids):
        """Populate predictions from Excel files

        TODO: Remove from player class

        Args:
            game_ids (list): List of tournament game id's
        """

        predictions = dict()
        root = self._settings.root
        excel_file = os.path.join(root, self._settings.data.dir, 'predictions',
                                  self.name + '.xls')
        json_file = os.path.join(root, self._settings.data.dir, 'predictions',
                                 self.name + '.json')
        mapping = read_json_to_attrdict(os.path.join(root, 'util', 'johroge_mapping.json'))
        excel_sheet = read_xls_to_class(excel_file).sheet_by_name('Tips')
        all_results_read = True

        for key in game_ids:
            tmp_dict = mapping(str(key))
            home = tmp_dict['home']
            away = tmp_dict['away']
            home_result = read_cell(excel_sheet, home[0], home[1])
            away_result = read_cell(excel_sheet, away[0], away[1])
            if home_result is not None and away_result is not None:
                predictions[key] = {'home': home_result, 'away': away_result}
            else:
                self._log.error('Could not read excel score {} at {}, {}'.format(key, home[0], home[1]))
                all_results_read = False
        if all_results_read:
            write_dict_to_json(predictions, json_file)


def read_cell(sheet, row, col):
    """Get score as cell value from excel sheet

    Args:
        sheet (xlrd.book.Book): Johroge excel sheet.
        row (int)
        col (int)

    Returns:
        score (int)
    """
    logger = logging.getLogger(__name__)
    cell = sheet.cell(row, col)
    score = None
    try:
        score = int(cell.value)
    except ValueError as err:
        logger.error(err)

    return score


def create_xls_mapping_help(filepath):
    """Fulhack to get data from Johroge's excel sheet"""
    excel = read_xls_to_class(filepath)
    bets = excel.sheet_by_name('Tips')
    predictions = list()
    for row_ind in range(bets.nrows):
        home = bets.row(row_ind)[3]
        away = bets.row(row_ind)[5]
        if home.ctype and home.ctype:
            predictions.append({'home_team': home.value, 'away_team': away.value,
                                'home_result': [row_ind, 7], 'away_result': [row_ind, 9]})
    return predictions


def main():
    FILENAME = '/home/jakob/dev/WednesdayWorldCup/data/predictions/test_raw.xls'
    excel_sheet = read_xls_to_class(FILENAME).sheet_by_name('Tips')

    print(read_cell(excel_sheet, 4, 9))


if __name__ == '__main__':
    main()

