#!/bin/bash

# Define the name of the Docker image and container
IMAGE_NAME="ytube-DLframe"
CONTAINER_NAME="youtube_dLoadApp"

# Function to check if container exists
check_container() {
    docker ps -aq -f name=^/${CONTAINER_NAME}$
}

# Function to stop and remove container if it exists
stop_remove_container() {
    if [ $(check_container) ]; then
        echo "Stopping and removing existing container..."
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
        echo "Existing container stopped and removed."
    fi
}

# Function to validate no conflicts before building
validate_no_conflicts() {
    if [ $(check_container) ]; then
        echo "Error: A container with the name $CONTAINER_NAME already exists."
        echo "Attempting to resolve conflict automatically..."
        stop_remove_container
        if [ $(check_container) ]; then
            echo "Automatic conflict resolution failed."
            echo "Please manually stop and remove any conflicting containers and try again."
            exit 1
        else
            echo "Conflict resolved successfully."
        fi
    fi
}

# Function to build the image
build_image() {
    echo "Building Docker image..."
    docker build -t $IMAGE_NAME .
    echo "Image built successfully."
}

# Function to run the container
run_container() {
    echo "Running Docker container..."
    docker run --name $CONTAINER_NAME -d -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $IMAGE_NAME
    echo "Container started successfully."
}

# Function to test the container
test_container() {
    echo "Testing if the container is up and running..."
    docker exec $CONTAINER_NAME echo "Container is operational."
}

# Menu system using whiptail
while true; do
    CHOICE=$(whiptail --title "Container Management Menu" --menu "Choose an option" 15 60 6 \
    "1" "Start or restart the container" \
    "2" "Connect to the container" \
    "3" "Stop and remove the container" \
    "4" "Rebuild the container image" \
    "5" "Test the container" \
    "6" "Exit" 3>&1 1>&2 2>&3)

    case $CHOICE in
        1)
            validate_no_conflicts
            build_image
            run_container
            ;;
        2)
            if [ $(check_container) ]; then
                docker exec -it $CONTAINER_NAME /bin/bash
            else
                echo "No container is currently running."
            fi
            ;;
        3)
            stop_remove_container
            echo "Container has been stopped and removed."
            ;;
        4)
            stop_remove_container
            validate_no_conflicts
            build_image
            echo "Image rebuilt. Ready to start the container."
            ;;
        5)
            if [ $(check_container) ]; then
                test_container
            else
                echo "Container is not running."
            fi
            ;;
        6)
            break
            ;;
        *)
            whiptail --msgbox "Invalid option: $CHOICE" 20 60 1
            ;;
    esac
done
