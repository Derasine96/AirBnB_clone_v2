#!/usr/bin/python3
"""A script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception=None):
    """Define a teardown function to remove the SQLAlchemy session."""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Method to list all states on a database"""
    states = storage.all("State").values()
    return render_template('9-states.html', state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """Displays an HTML page with info about <id>, if it exists."""
    states = storage.all("State").values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
