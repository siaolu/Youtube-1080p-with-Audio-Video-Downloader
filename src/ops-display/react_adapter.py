# react_adapter.py
# Version 0.54
# Manages the integration of React-based frontend with Flask, setting up necessary routes for serving the application and handling API requests.

from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder='build')

@app.route('/')
def serve_home():
    """
    Serve the main index.html from the React build directory.
    Returns:
        Response: Sends the index.html as the response.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/data')
def api_data():
    """
    API endpoint to provide data to the frontend.
    Returns:
        Response: JSON object containing data for the frontend.
    """
    data = {'message': 'Data fetched successfully'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True)


"""
# Example usage within a Flask app context 
# (this would be moved to the appropriate part of app_main.py)
# app = Flask(__name__, static_folder='path_to_react_build')
# react_adapter = ReactAdapter(app)

"""
