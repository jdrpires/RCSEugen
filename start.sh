#!/bin/bash

echo "Starting RCS API with Docker..."
docker-compose up --build -d

echo "Waiting for services to start..."
sleep 5

echo "API is running at http://localhost:8080"
echo "Swagger documentation is available at http://localhost:8080/docs"
echo "ReDoc documentation is available at http://localhost:8080/redoc"

echo "To view logs, run: docker-compose logs -f"
echo "To stop the services, run: docker-compose down"
