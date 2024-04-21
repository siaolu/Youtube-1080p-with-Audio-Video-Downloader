#set
#!/bin/bash

# Define the name of the Docker image and container
IMAGE_NAME="youtube_downloader"
CONTAINER_NAME="youtube_downloader_app"

# Stop and remove any existing container with the same name
echo "Checking if container exists..."
if [ $(docker ps -aq -f name=^/${CONTAINER_NAME}$) ]; then
    echo "Container exists. Removing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Run the Docker container
echo "Running Docker container..."
docker run --name $CONTAINER_NAME -d -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix $IMAGE_NAME

echo "Container started successfully. YouTube Downloader is running."
