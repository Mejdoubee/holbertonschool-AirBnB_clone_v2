#!/usr/bin/python3
'''
0-hello_route module
This module starts a Flask web application with a 5 routes.
The web application listens on 0.0.0.0, port 5000.
'''
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_HBNB():
    '''
    Returns a string "Hello HBNB!" when the route / is accessed
    '''
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def HBNB():
    '''
    Returns a string "HBNB" when the route /hbnb is accessed
    '''
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def C_text(text):
    '''
    Returns a string "C " followed by the value of the text variable
    when the route /c/<text> is accessed
    '''
    return "C " + text.replace('_', ' ')


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def Python_text(text="is cool"):
    '''
    Returns a string "Python " followed by the value of
    the text variable(The default value of text is “is cool”)
    when the route /python/<text> is accessed
    '''
    return "Python " + text.replace('_', ' ')


@app.route("/number/<int:n>", strict_slashes=False)
def number_n(n):
    '''
    Returns “n is a number” only if n is an integer
    '''
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    '''
    Returns a HTML page only if n is an integer
    '''
    return render_template('5-number.html', number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def number_odd_or_even(n):
    '''
    Returns a HTML page only if n is an integer
    '''
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
