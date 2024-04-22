#!/bin/bash

# Define the name of the Docker image and container
IMAGE_NAME="ytube-DLframe"
CONTAINER_NAME="youtube_dLoadApp"

# Check if the Docker container exists
function check_container() {
    docker ps -aq -f name=^/${CONTAINER_NAME}$
}

# Stop and remove the container if it exists
function stop_remove_container() {
    if [ "$(check_container)" ]; then
        echo "Stopping and removing existing container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    fi
}

# Build the Docker image
function build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
    echo "Image built successfully."
}

# Run the Docker container
function run_container() {
    echo "Running Docker container..."
    docker run --name $CONTAINER_NAME -d -p 5000:5000 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $IMAGE_NAME
    echo "Container started successfully."
}

# Check for container logs
function check_logs() {
    echo "Fetching logs from the container..."
    docker logs $CONTAINER_NAME
}

# Function to handle menu selection
function menu() {
    echo "Please select an option:"
    echo "1) Build and Run Container"
    echo "2) Stop and Remove Container"
    echo "3) Rebuild Container"
    echo "4) View Container Logs"
    echo "5) Exit"
    read option

    case $option in
        1)
            stop_remove_container
            build_image
            run_container
            ;;
        2)
            stop_remove_container
            ;;
        3)
            stop_remove_container
            build_image
            ;;
        4)
            check_logs
            ;;
        5)
            exit 0
            ;;
        *)
            echo "Invalid option. Please try again."
            ;;
    esac
}

# Main loop to show the menu repeatedly
while true; do
    menu
done
