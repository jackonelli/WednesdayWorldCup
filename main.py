import os
import logging
from datetime import datetime
from lib.tournament import Tournament
from lib.player import Player
from util.io import read_json_to_attrdict
from util.log import setup_logger
from lib.model import PoissonGammaModel
from lib.fifa_table_parser import get_stats, get_totals
from lib.game import Game

META_SETTINGS = 'settings/meta.json'
logger = logging.getLogger(__name__)


def main():
    settings = read_json_to_attrdict(META_SETTINGS)
    log_file = '{}.log'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    setup_logger(log_path=os.path.join(settings.root, settings.logdir,  log_file))
    tournament = Tournament(settings)
    tournament.populate()
    #tournament.generate_dummy_results(fix_seed=True, playoff=True)
    #tournament.evaluate()
    player = Player(settings, 'test')
    #player.epa_data_from_xls(tournament.games.keys())
    player.predictions_from_json()
    #  tournament.generate_results_from_predictions(player.predictions)
    #  tournament.evaluate()
    paul = PoissonGammaModel('data/team_stats.json')
    paul.set_prior_params()
    #for group in tournament.groups.values():
    #    for game in group.games:
    #        paul.sample_game_score(game)
    #        game.finished = True
    #        print(game)
    fra = 9
    kro = 15
    uru = 4
    por = 5
    bra = 17
    mex = 22
    bel = 25
    pol = 29
    ksa = 2
    spa = 6
    arg = 13
    den = 12
    ger = 21
    ser = 20
    col = 31
    eng = 28
    egy = 3
    swe = 23
    jap = 32
    sen = 30
    nig = 16
    sui = 18

    home_id = spa
    away_id = bra
    home = tournament.teams[home_id]
    away = tournament.teams[away_id]
    game = tournament.games[1]
    game.home_team = home
    game.away_team = away
    paul.sample_game_score(game)
    game.finished
    print(repr(game))



if __name__ == '__main__':
    main()
