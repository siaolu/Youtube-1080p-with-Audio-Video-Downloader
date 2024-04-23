# utils.py
# Version 0.53
# Provides utility functions for file operations, database access, and other common tasks,
# ensuring compatibility and integration with the application's latest architecture.

import os
import json
import sqlite3
from flask import g
from config import DATABASE_URI

def load_config(path='settings.json'):
    """
    Load configuration settings from a JSON file.
    
    Args:
        path (str): Path to the configuration file.
        
    Returns:
        dict: Configuration settings.
    """
    with open(path, 'r') as file:
        return json.load(file)

def safe_operation(func):
    """
    Decorator to handle exceptions and log errors for any utility function.
    
    Args:
        func (callable): Function to be decorated.
        
    Returns:
        callable: Wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error during {func.__name__}: {str(e)}")
            return None
    return wrapper

@safe_operation
def read_file(file_path):
    """
    Reads content from a file.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()

def get_db():
    """
    Retrieve or create a database connection for the current application context.
    
    Returns:
        sqlite3.Connection: SQLite database connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_URI)
        g.db.row_factory = sqlite3.Row
    return g.db

from contextlib import contextmanager

@contextmanager
def managed_file(file_path, mode='r'):
    """
    Context manager for file operations, ensuring proper closure after use.
    
    Args:
        file_path (str): File path.
        mode (str): Mode in which to open the file.
        
    Yields:
        _io.TextIOWrapper: Opened file object.
    """
    file = open(file_path, mode)
    try:
        yield file
    finally:
        file.close()
