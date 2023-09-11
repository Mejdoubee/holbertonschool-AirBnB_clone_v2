#!/usr/bin/python3
'''
script that starts a Flask web application
'''
from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    '''
    Close the session after each request
    '''
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def _display_cities_by_states():
    '''
    Display states and their cities
    '''
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    return render_template('cities_by_states.html', states=sorted_states)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
