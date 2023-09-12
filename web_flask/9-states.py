#!/usr/bin/python3
'''
script that starts a Flask web application
'''
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """remove the current SQLAlchemy Session: """
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """display all the states"""
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """display the state and its cities by its ID"""
    all_states = storage.all(State).values()
    for state in all_states:
        if state.id == id:
            return render_template(
                '9-states.html', state=state, s_cities=state.cities
                )
    return render_template('9-states.html', state_not_found=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
