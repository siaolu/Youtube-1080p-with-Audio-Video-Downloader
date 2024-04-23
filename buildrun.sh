#!/bin/bash

# buildrun.sh
# Version 4.3
# Script to manage Docker images and containers, including operations to build, run, remove, and retrieve logs.

IMAGE_NAME="myapp"
CONTAINER_NAME="myapp_container"

function list_images() {
    echo "Available Docker images:"
    docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>"
}

function select_and_run_image() {
    echo "Select an image to run:"
    list_images
    read -p "Enter the image name and tag (e.g., repository:tag): " image_selection
    if [ -z "$image_selection" ]; then
        echo "No image selected, exiting."
        exit 1
    else
        docker run -d --name $CONTAINER_NAME -p 80:80 "$image_selection"
        echo "Container started from image $image_selection"
    fi
}

function build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
    echo "Docker image built successfully."
}

function remove_all_images() {
    echo "Removing all Docker images..."
    docker rmi $(docker images -a -q)
    echo "All Docker images removed."
}

function remove_all_containers() {
    echo "Stopping and removing all Docker containers..."
    docker rm $(docker ps -aq)
    echo "All Docker containers removed."
}

function get_container_logs() {
    echo "Available running containers:"
    docker ps --format "{{.Names}}"
    read -p "Enter the container name to retrieve logs: " container_name
    if [ -z "$container_name" ]; then
        echo "No container selected, exiting."
        exit 1
    else
        docker logs $container_name
    fi
}

function stop_and_remove_container() {
    echo "Stopping container..."
    docker stop $CONTAINER_NAME
    echo "Removing container..."
    docker rm $CONTAINER_NAME
}

function restart_container() {
    echo "Restarting Docker container..."
    docker restart $CONTAINER_NAME
    echo "Container restarted successfully."
}

echo "Select an option:"
echo "1) Build and Run"
echo "2) Stop and Remove Container"
echo "3) Restart Container"
echo "4) List and Run Image"
echo "5) Remove All Images"
echo "6) Remove All Containers"
echo "7) Get Container Logs"
echo "8) Exit"
read -p "Enter choice: " choice

case $choice in
    1)
        build_image
        select_and_run_image
        ;;
    2)
        stop_and_remove_container
        ;;
    3)
        restart_container
        ;;
    4)
        select_and_run_image
        ;;
    5)
        remove_all_images
        ;;
    6)
        remove_all_containers
        ;;
    7)
        get_container_logs
        ;;
    8)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice, exiting."
        exit 1
        ;;
esac
