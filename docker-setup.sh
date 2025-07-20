#!/bin/bash

# Docker Hub Login
echo "Logging into Docker Hub..."
docker login -u preetraval45@gmail.com -p Arjuntower@231

if [ $? -eq 0 ]; then
    echo "Successfully logged into Docker Hub"
else
    echo "Failed to login to Docker Hub"
    exit 1
fi

# Build and push backend image
echo "Building and pushing backend image..."
docker build -t preetraval45/cipherquest-backend:latest ./backend
docker push preetraval45/cipherquest-backend:latest

# Build and push frontend image
echo "Building and pushing frontend image..."
docker build -t preetraval45/cipherquest-frontend:latest ./frontend
docker push preetraval45/cipherquest-frontend:latest

echo "Docker images built and pushed successfully!"
echo "You can now run: docker-compose up --build" 