#!/bin/bash

# Test the health check endpoint
echo "Testing health check endpoint..."
curl -X GET http://localhost:8000/api/v1/health

echo -e "\n\n"

# Test the generate synthetic network endpoint
echo "Testing generate synthetic network endpoint..."
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

echo -e "\n"
