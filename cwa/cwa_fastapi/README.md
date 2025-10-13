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

### Docker Exec

You can also use docker exec to call the API from within the container:
```bash
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
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
- **models.py**: SQLAlchemy ORM models
- **schemas.py**: Pydantic models for request/response validation
- **database.py**: Database connection and session management

## Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **GeoAlchemy2**: Spatial extension for SQLAlchemy
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server implementation
- **PostGIS**: Spatial database extension for PostgreSQL
