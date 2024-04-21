# Use an Ubuntu base image that includes X11 libraries
FROM ubuntu:20.04

# Set environment variables to avoid interactive dialog during build
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary packages including minimal X components and Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    xauth \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Setup for X11 forwarding for GUI support
ENV DISPLAY=:99
RUN Xvfb :99 -screen 0 1024x768x16 &

# Define entrypoint to launch the application
ENTRYPOINT ["python3", "./main_gui.py"]
