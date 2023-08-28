#!/usr/bin/python3
'''Flask web application that lists states from the database'''
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    '''Route that displays a list of all State objects present in DBStorage'''
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(exception):
    '''After each request, this function provides the ability to
    close the current SQLAlchemy Session'''
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
