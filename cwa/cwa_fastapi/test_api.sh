#!/bin/bash

# Test the health check endpoint
echo "Testing health check endpoint..."
curl -X GET http://localhost:8000/api/v1/health

echo -e "\n\n"

# Test the generate synthetic network endpoint
echo "Testing generate synthetic network endpoint..."
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

echo -e "\n\n"

# Test the load to Neo4j endpoint
echo "Testing load to Neo4j endpoint..."
curl -X POST http://localhost:8000/api/v1/load-to-neo4j

echo -e "\n\n"

# Test the verify Neo4j endpoint
echo "Testing verify Neo4j endpoint..."
curl -X GET http://localhost:8000/api/v1/verify-neo4j

echo -e "\n"
