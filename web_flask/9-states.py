#!/usr/bin/python3
'''
script that starts a Flask web application
'''
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    '''
    Display a list of all states
    '''
    states_sorted = sorted(
        storage.all(State).values(), key=lambda state: state.name
    )
    return render_template('7-states_list.html', states=states_sorted)


@app.route('/states/<id>', strict_slashes=False)
def state_and_cities(id):
    '''
    Display a state and its cities
    '''
    state = storage.get(State, id)
    if state:
        cities_sorted = sorted(state.cities, key=lambda city: city.name)
        return render_template("9-states.html", state=state, cities=cities_sorted)
    else:
        return render_template("9-states.html", state=None)


@app.teardown_appcontext
def teardown_db(exception=None):
    '''
    Close the session after each request
    '''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
