# General Media download

## Description
This application is designed to manage media downloads and processing, offering a user-friendly interface for downloading videos, extracting audio, and managing media files efficiently. It leverages a modular architecture with support for multiple display types including terminal-based interfaces and web-based frontends.

## Features
- Download videos from YouTube.
- Extract audio from downloaded videos.
- Serve a web interface using React for easy interaction.
- CLI-based interaction for terminal users.

## System Requirements
- Python 3.9 or higher
- Docker
- Flask
- Pytube, moviepy for media handling
- React (optional for web frontend)

## Setup Instructions

### Installing Dependencies
1. Ensure Python and Docker are installed on your system.
2. Clone the repository to your local machine.
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
