# utils.py
import os
import logging
import yaml

def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration from a YAML file.
    """
    path = os.getenv(env_key, default_path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def load_config(config_file='app_config.yaml'):
    """
    Load application configuration from a YAML file.
    """
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        return config
    else:
        raise FileNotFoundError(f"No configuration file found at {config_file}")

def safe_file_operation(func):
    """
    Decorator to perform safe file operations with exception handling.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"File operation failed: {e}")
            return None
    return wrapper

@safe_file_operation
def save_to_file(file_path, data):
    """
    Save data to a file safely.
    """
    with open(file_path, 'w') as file:
        file.write(data)

@safe_file_operation
def read_from_file(file_path):
    """
    Read data from a file safely.
    """
    with open(file_path, 'r') as file:
        return file.read()
