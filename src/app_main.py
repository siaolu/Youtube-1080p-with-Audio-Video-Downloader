# app_main.py
# Version 0.55
# Enhances the Flask application by adding more robust error handling, scalability improvements, and better integration with external services.

from flask import Flask, jsonify, request
import asyncio
from config import close_db
from media_downloads import download_video, extract_audio, extract_video_metadata

app = Flask(__name__)

@app.teardown_appcontext
def close_database(exception=None):
    """
    Ensure database connections are closed after request processing.
    Args:
        exception (Exception, optional): Any exception that might have occurred during the request.
    """
    close_db(exception)

@app.route('/process_video', methods=['POST'])
async def process_video():
    """
    Asynchronously handle video processing requests.
    Expects JSON input containing 'url' and 'output_path' keys.

    Returns:
        JSON response with the filename of the downloaded video or an error message.
    """
    url = request.json.get('url')
    output_path = request.json.get('output_path')
    if url and output_path:
        try:
            filename = await download_video(url, output_path)
            return jsonify({'filename': filename}), 200
        except Exception as e:
            app.logger.error(f"Failed to process video: {e}")
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'URL and output path are required'}), 400

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)  # Necessary for proper asyncio support in Flask
