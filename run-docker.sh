#!/bin/bash

echo "Building Flask app Docker image..."
docker build -t flask-hello-world .

echo "Running Flask app container..."
docker run -p 8080:9696 -d --name flask-app flask-hello-world

echo "Flask app is running at http://localhost:8080"
echo "To stop: docker stop flask-app && docker rm flask-app" 