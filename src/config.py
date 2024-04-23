
# app_main.py
# Version 0.54
# Handles web requests and delegates tasks for media processing. Updated to ensure robust error handling and asynchronous operation.

"""" >>> *** Key Features in config.py:
summary: config.py  *** >>> Key Changes and Implementations:

Logging Configuration: Set up basic logging for the application, 
which is crucial for monitoring and debugging.

Database Connection Handling: get_db() manages database 
connections efficiently using Flask's application context, 
ensuring that database connections are properly managed 
without leaks.

Database Closing Function: close_db() is defined to close the 
database connection explicitly when the application context is
destroyed, preventing any potential issues with open connections.

Database Initialization: init_db() sets up the database tables
according to the schema provided in a SQL file, simplifying 
database setup and maintenance.

Flask CLI Integration: The init_db_command function provides a
command-line interface to initialize the database directly from
the command line using Flask's CLI capabilities, facilitating
easy setup during deployment or development.

"""
# config.py
# Version 0.53
# Manages configuration settings and database connections for the Flask application, with enhanced support for asynchronous operations and connection pooling.

import os
import sqlite3
from flask import g, current_app
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Determine the environment and set the database URI accordingly
ENVIRONMENT = os.getenv('FLASK_ENV', 'development')
DATABASE_URI = {
    'development': 'sqlite:///dev.db',
    'testing': 'sqlite:///test.db',
    'production': os.getenv('DATABASE_URL')
}.get(ENVIRONMENT, 'sqlite:///dev.db')

def get_db():
    """
    Retrieve a database connection from the pool for the current application context, ensuring efficient management of connections.
    
    Returns:
        sqlite3.Connection: SQLite database connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_URI, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Close the database connection at the end of the request if it exists.
    
    Args:
        e (Exception, optional): Exception that was raised during the request, if any.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Initializes the database using a schema file appropriate for the current environment.
    """
    db = get_db()
    with current_app.open_resource(f'schema_{ENVIRONMENT}.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init-db')
def init_db_command():
    """
    Flask CLI command to initialize the database. Clears existing data and creates new tables based on the environment-specific schema.
    """
    init_db()
    print('Initialized the database.')

# Ensure that the configuration and database operations are appropriate for the Flask application's current environment.
if __ENVIRONMENT == 'production':
    logging.setLevel(logging.WARNING)
