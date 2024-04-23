#!/bin/bash

# buildrun.sh
# Version 4.1
# This script manages Docker operations such as build, run, stop, and restart with added health checks and error handling.

IMAGE_NAME="myapp"
CONTAINER_NAME="myapp_container"

function build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME . || { echo "Docker build failed"; exit 1; }
}

function run_container() {
    echo "Running Docker container..."
    docker run -d --name $CONTAINER_NAME -p 80:80 $IMAGE_NAME || { echo "Docker run failed"; exit 1; }
    echo "Checking container health..."
    check_health
}

function stop_container() {
    echo "Stopping Docker container..."
    docker stop $CONTAINER_NAME || { echo "Docker stop failed"; exit 1; }
}

function remove_container() {
    echo "Removing Docker container..."
    docker rm $CONTAINER_NAME || { echo "Docker remove failed"; exit 1; }
}

function restart_container() {
    echo "Restarting Docker container..."
    docker restart $CONTAINER_NAME || { echo "Docker restart failed"; exit 1; }
}

function check_health() {
    for i in {1..5}; do
        health=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME)
        if [ "$health" = "healthy" ]; then
            echo "Container is healthy."
            return
        else
            echo "Waiting for container to become healthy..."
            sleep 10
        fi
    done
    echo "Container did not become healthy."
    exit 1
}

echo "Select an option:"
echo "1) Build and Run"
echo "2) Stop and Remove"
echo "3) Restart"
echo "4) Exit"
read -p "Enter choice: " choice

case $choice in
  1)
    build_image
    run_container
    ;;
  2)
    stop_container
    remove_container
    ;;
  3)
    restart_container
    ;;
  4)
    exit 0
    ;;
  *)
    echo "Invalid choice, exiting."
    exit 1
    ;;
esac
