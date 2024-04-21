# app_main.py
from flask import Flask, jsonify, send_from_directory
from ops-display.display_factory import get_display_adapter
import os
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flask app initialization
app = Flask(__name__, static_folder='build')

# Argument parser setup for runtime configuration
parser = argparse.ArgumentParser(description="Run the application with specified display type.")
parser.add_argument('--display', type=str, help='Display type: curses, pysimplegui, or react', default='curses')
args = parser.parse_args()

# Fetch display type from command line arguments or default to 'curses'
DISPLAY_TYPE = args.display

def initialize_display():
    """ Initialize display based on the configured display type. """
    try:
        display_adapter = get_display_adapter(DISPLAY_TYPE)
        display_adapter.initialize()
        return display_adapter
    except Exception as e:
        logging.error(f"Failed to initialize display adapter: {e}")
        raise

@app.route('/')
def index():
    """ Serve the main index.html from React build directory if using React. """
    if DISPLAY_TYPE == 'react':
        return send_from_directory(app.static_folder, 'index.html')
    else:
        return "This service is not configured to use a web-based interface."

@app.route('/api/data')
def get_data():
    """ API endpoint to get data for the React app or any other AJAX-based frontend. """
    data = "Dynamic data from the backend"
    return jsonify({'data': data})

def main():
    display = None
    try:
        display = initialize_display()
        if DISPLAY_TYPE in ['curses', 'pysimplegui']:
            while True:
                data = "Update this with actual data processing logic"
                display.update(data)
        elif DISPLAY_TYPE == 'react':
            app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logging.error(f"Error running the application: {e}")
    finally:
        if display:
            display.shutdown()

if __name__ == "__main__":
    main()
