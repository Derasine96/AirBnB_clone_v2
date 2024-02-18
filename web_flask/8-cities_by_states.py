#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception=None):
    """Define a teardown function to remove the SQLAlchemy session."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def list_cities():
    """Method to list all states on a database"""
    states = storage.all("State").values()
    cities = storage.all("City"). values()
    return render_template('7-states_list.html', cities=cities, states=states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
