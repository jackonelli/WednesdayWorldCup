import os
import logging
from _datetime import datetime
from lib.tournament import Tournament
from lib.player import Player
from util.io import read_json_to_attrdict
from util.log import setup_logger
import random
META_SETTINGS = 'settings/meta.json'
logger = logging.getLogger(__name__)


def main():
    settings = read_json_to_attrdict(META_SETTINGS)
    log_file = '{}.log'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    setup_logger(log_path=os.path.join(settings.root, settings.logdir,  log_file))
    tournament = Tournament(settings)
    tournament.populate()
    tournament.groups['A'].winner = tournament.groups['A'].teams[0]
    tournament.groups['A'].runner_up = tournament.groups['A'].teams[1]
    tournament.groups['A'].finished = True

    tournament.groups['B'].winner = tournament.groups['B'].teams[1]
    tournament.groups['B'].runner_up = tournament.groups['B'].teams[0]
    tournament.groups['B'].finished = True

    tournament.playoff.fill_games(tournament.teams, tournament.groups, tournament.games)
    tournament.print_playoff()

    #  tournament.generate_dummy_results()


if __name__ == '__main__':
    main()
