# app_main.py
# Version 0.53
# Incorporates enhancements for handling asynchronous media downloading tasks and improved database management.

from flask import Flask, jsonify, request, g, current_app
import sqlite3
import asyncio
from config import get_db, statlogtimer
import media_downloads

app = Flask(__name__)

DATABASE_URI = 'sqlite:///session.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/process_video', methods=['POST'])
@statlogtimer
async def process_video():
    """API endpoint to asynchronously process a video download."""
    url = request.json.get('url')
    output_path = request.json.get('output_path')
    if url and output_path:
        try:
            filename = await media_downloads.download_video(url, output_path)
            return jsonify({'filename': filename}), 200
        except Exception as e:
            current_app.logger.error(f"Failed to process video: {e}")
            return jsonify({'error': 'Failed to process video'}), 500
    else:
        return jsonify({'error': 'URL and output path are required'}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # use_reloader=False is important for running asyncio in Flask
