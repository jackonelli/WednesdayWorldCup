import os
import logging
from datetime import datetime
from lib.tournament import Tournament
from lib.player import Player
from util.io import read_json_to_attrdict
from util.log import setup_logger
META_SETTINGS = 'settings/meta.json'
logger = logging.getLogger(__name__)


def main():
    settings = read_json_to_attrdict(META_SETTINGS)
    settings['root'] = '/home/jakob/dev/WednesdayWorldCup'
    log_file = '{}.log'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    setup_logger(log_path=os.path.join(settings.root, settings.logdir,  log_file))
    tournament = Tournament(settings)
    tournament.populate()
    #tournament.generate_dummy_results(fix_seed=True, playoff=True)
    #tournament.evaluate()
    player = Player(settings, 'test_raw')
    player.epa_data_from_xls(tournament.games.keys())
    player.predictions_from_json()


if __name__ == '__main__':
    main()
