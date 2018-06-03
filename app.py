from util.io import read_json_to_attrdict
from lib.tournament import Tournament
from flask import Flask, render_template

app = Flask(__name__)
META_SETTINGS = 'settings/meta.json'


@app.route('/')
def tournament():
    settings = read_json_to_attrdict(META_SETTINGS)
    world_cup = Tournament(settings)
    world_cup.populate()
    #world_cup.generate_dummy_results()
    #world_cup.evaluate()

    return render_template('index.html', tournament=world_cup)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
