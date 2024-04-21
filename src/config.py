# config.py
import os

# Helper function to convert environment variable strings to boolean
def str_to_bool(v):
    return v.lower() in ("yes", "true", "t", "1")

# Base configuration
class Config:
    DEBUG = str_to_bool(os.getenv('DEBUG', 'False'))
    PORT = int(os.getenv('PORT', 5000))
    DISPLAY_TYPE = os.getenv('DISPLAY_TYPE', 'curses')  # Default display type
    STATIC_FOLDER = os.getenv('STATIC_FOLDER', 'build')  # Default folder for static files

# Development specific configuration
class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.getenv('DEV_DATABASE_URI', 'sqlite:///dev.db')

# Testing specific configuration
class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.getenv('TEST_DATABASE_URI', 'sqlite:///test.db')

# Production specific configuration
class ProductionConfig(Config):
    DEBUG = False
    PORT = int(os.getenv('PORT', 80))
    DATABASE_URI = os.getenv('PROD_DATABASE_URI', 'sqlite:///prod.db')

# Dictionary to hold configurations for different environments
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

# Function to get the appropriate config class based on the environment
def get_config(config_name):
    return config_by_name.get(config_name, Config)

# Example usage:
# current_config = get_config(os.getenv('FLASK_ENV', 'dev'))
