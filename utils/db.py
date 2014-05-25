import flask
import oursql
from app import app
from core.settings import SETTINGS


def connect_db():
    return oursql.connect(**SETTINGS['DB_CONFIG'])


def get_db():
    """Returns the current database connection if one exists, otherwise a new
    one is created.
    """
    if not hasattr(flask.g, 'db_connection'):
        flask.g.db_connection = connect_db()
    return flask.g.db_connection


@app.teardown_appcontext
def close_db(error):
    """Closes the database connection when the request is completed."""
    if hasattr(flask.g, 'db_connection'):
        flask.g.db_connection.close()


