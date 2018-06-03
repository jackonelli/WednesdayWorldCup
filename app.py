import os
import logging
from datetime import datetime
from util.log import setup_logger
from util.io import read_json_to_attrdict
from lib.tournament import Tournament
from flask import Flask, render_template

app = Flask(__name__)
logger = logging.getLogger(__name__)
META_SETTINGS = 'settings/meta.json'


@app.route('/')
def tournament():
    settings = read_json_to_attrdict(META_SETTINGS)
    log_file = '{}.log'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    setup_logger(log_path=os.path.join(settings.root, settings.logdir,  log_file))

    world_cup = Tournament(settings)
    world_cup.populate()
    world_cup.generate_dummy_results(playoff=True)
    world_cup.evaluate()

    return render_template('index.html', tournament=world_cup)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
