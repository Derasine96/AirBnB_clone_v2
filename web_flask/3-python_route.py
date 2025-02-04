#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """A function that displays a text"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def index():
    """A function that displays a text"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_info(text):
    """A function that displays a text"""
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_info(text):
    """A function that displays a text"""
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
