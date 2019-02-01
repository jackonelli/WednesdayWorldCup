from app import app
from flask import render_template
from lib.tournament import Tournament
from lib.player import Player

@app.route('/')
@app.route('/index')
def tournament():
    settings = app.config['SETTINGS']
    settings['root'] = app.config['ROOT']
    world_cup = Tournament(settings)
    world_cup.populate()
#    world_cup.evaluate()

    return render_template('index.html', tournament=world_cup)
