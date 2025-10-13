# CWA FastAPI Application

This is the FastAPI-based implementation of the Clean Water Analytics toolkit, providing REST API endpoints for water network operations.

## Overview

The FastAPI application provides a modern, high-performance alternative to the Django-based implementation, focusing on API-first design and ease of use.

## Features

- **RESTful API**: Clean, modern REST endpoints
- **Interactive Documentation**: Automatic OpenAPI/Swagger documentation at `/docs`
- **High Performance**: Built on FastAPI with async support
- **Database Integration**: Uses SQLAlchemy with GeoAlchemy2 for PostGIS integration
- **Synthetic Network Generation**: Create test water networks with a single API call

## API Endpoints

### Health Check
- **Endpoint**: `GET /api/v1/health`
- **Description**: Check if the API is running
- **Response**: 
  ```json
  {
    "status": "ok",
    "message": "FastAPI server is running"
  }
  ```

### Generate Synthetic Network
- **Endpoint**: `POST /api/v1/generate-synthetic-network`
- **Description**: Generate a synthetic water network with pipes, hydrants, valves, and flow data
- **Response**: 
  ```json
  {
    "status": "success",
    "message": "Successfully generated synthetic network",
    "pipes_created": 22,
    "hydrants_created": 11,
    "valves_created": 7,
    "flow_records_created": 22
  }
  ```

### Load Network to Neo4j
- **Endpoint**: `POST /api/v1/load-to-neo4j`
- **Description**: Load the water network from PostGIS into Neo4j graph database
- **Response**: 
  ```json
  {
    "status": "success",
    "message": "Successfully loaded network into Neo4j",
    "pipes_loaded": 22
  }
  ```

### Verify Neo4j Data
- **Endpoint**: `GET /api/v1/verify-neo4j`
- **Description**: Verify that data has been loaded into Neo4j
- **Response**: 
  ```json
  {
    "status": "success",
    "message": "Neo4j database contains data",
    "node_count": 125,
    "relationship_count": 200
  }
  ```

## Usage

### With Docker Compose

The FastAPI server starts automatically when you run:
```bash
docker-compose up -d
```

### Access the API

1. **Interactive Documentation**: http://localhost:8000/docs
2. **Health Check**: 
   ```bash
   curl http://localhost:8000/api/v1/health
   ```
3. **Generate Network**: 
   ```bash
   curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
   ```
4. **Load to Neo4j**: 
   ```bash
   curl -X POST http://localhost:8000/api/v1/load-to-neo4j
   ```
5. **Verify Neo4j**: 
   ```bash
   curl http://localhost:8000/api/v1/verify-neo4j
   ```

### Docker Exec

You can also use docker exec to call the API from within the container:
```bash
# Generate synthetic network
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Load to Neo4j
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/load-to-neo4j

# Verify Neo4j data
docker exec udtcwafastapi curl http://localhost:8000/api/v1/verify-neo4j
```

## Development

### Local Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export POSTGIS_DB_NAME__ENV_VAR=postgis
   export POSTGIS_DB_USER__ENV_VAR=postgis
   export POSTGIS_DEFAULT_DB_HOST__ENV_VAR=localhost
   export POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR=postgis
   export POSTGIS_DEFAULT_PORT__ENV_VAR=5432
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Architecture

- **main.py**: FastAPI application entry point
- **routes.py**: API endpoint definitions and business logic
- **models.py**: SQLAlchemy ORM models with GeoAlchemy2 for spatial data
- **database.py**: Database connection configuration for PostGIS and Neo4j
- **gis_to_neo4j_adapter.py**: Compatibility layer for loading GIS data to Neo4j
- **config_validator.py**: Pydantic-based configuration validation (Django-free)
- **schemas.py**: Pydantic models for request/response validation
- **constants.py**: Application constants
- **schemas.py**: Pydantic models for request/response validation
- **database.py**: Database connection and session management

## Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **GeoAlchemy2**: Spatial extension for SQLAlchemy
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation
- **PostGIS**: Spatial database extension for PostgreSQL
- **Neo4j**: Graph database for network analysis
- **Neomodel**: Object-Graph Mapper for Neo4j
- **NetworkX**: Python package for complex networks
- **cleanwater (cwm)**: Core water network transformation library

## Dependencies

The FastAPI application requires the following key dependencies:

1. **Core FastAPI dependencies** - defined in `requirements.txt`
2. **cleanwater package (cwm)** - installed from the `/opt/udt/cwm` directory in the Docker container
3. **Django** - required by the cleanwater package for GIS transformations (though the FastAPI app itself doesn't use Django)

The Dockerfile handles the installation of all dependencies, including the cleanwater package.
