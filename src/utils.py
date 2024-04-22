# utils.py
import os
import json
import logging
from contextlib import contextmanager

# Setup logging configuration
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

# Load configuration from a JSON file
def load_config(file_path):
    """
    Load configuration data from a JSON file.
    Args:
        file_path (str): The path to the configuration file.
    Returns:
        dict: Configuration data.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return {}

# Safe file operation decorator for error handling
def safe_file_operation(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error during file operation in {func.__name__}: {e}")
            raise
    return wrapper

@safe_file_operation
def write_to_file(file_path, data):
    """
    Writes data to a file.
    Args:
        file_path (str): The path to the file where data will be written.
        data (str): The data to write.
    """
    with open(file_path, 'w') as file:
        file.write(data)

@safe_file_operation
def read_from_file(file_path):
    """
    Reads data from a file.
    Args:
        file_path (str): The path to the file to read from.
    Returns:
        str: The contents of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()

# Context manager for managing resources, illustrating performance improvement
@contextmanager
def managed_file(file_path, mode='r'):
    """
    Context manager for opening and closing files safely.
    Args:
        file_path (str): The path to the file.
        mode (str): Mode in which the file will be opened.
    Yields:
        _io.TextIOWrapper: The file object.
    """
    try:
        resource = open(file_path, mode)
        yield resource
    finally:
        resource.close()

# Example of using the managed file context manager
def read_large_file(file_path):
    """
    Reads a large file line by line using a context manager.
    Args:
        file_path (str): The path to the large file.
    Yields:
        str: Each line from the file.
    """
    with managed_file(file_path, 'r') as file:
        for line in file:
            yield line.strip()

# Set up logging at the desired level (could be set via config or env var)
setup_logging(logging.DEBUG)
