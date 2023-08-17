#!/usr/bin/python3
'''
0-hello_route module
This module starts a Flask web application with a single route.
The web application listens on 0.0.0.0, port 5000.
'''
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    '''
    Returns a string "Hello HBNB!" when the route / is accessed
    '''
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
