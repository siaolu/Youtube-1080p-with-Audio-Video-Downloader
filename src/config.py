# config.py
# Version 0.52
# Handles configuration settings and database connections for the application.

import sqlite3
from flask import g, current_app
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_URI = 'sqlite:///session.db'

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE_URI,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """If this request connected to the database, close the connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with a schema."""
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Flask CLI command to initialize the database."""
    init_db()
    print('Initialized the database.')
