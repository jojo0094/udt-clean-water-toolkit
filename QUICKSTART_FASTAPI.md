# Quick Start Guide - FastAPI Implementation

This guide shows how to use the new FastAPI implementation for generating synthetic water networks.

## What's New?

The toolkit now includes a **FastAPI-based REST API** that provides the same synthetic network generation capabilities as the Django management command, but accessible via HTTP endpoints.

## Prerequisites

- Docker and Docker Compose installed
- `.env` file configured (see main README.md)

## Getting Started

### 1. Start the Services

```bash
docker-compose up -d
```

This will start:
- PostGIS database (port 5432)
- Neo4j database (ports 7474, 7687)
- Django application (cwageodjango container)
- **FastAPI application (port 8000)** ⭐ NEW!
- Orchestrator for initial setup

### 2. Wait for Initialization

Monitor the orchestrator logs to ensure setup is complete:

```bash
docker-compose logs -f orchestrator
```

Wait until you see messages about migrations being applied.

### 3. Access the FastAPI Application

#### Option A: Interactive API Documentation (Recommended for Testing)

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

From the Swagger UI, you can:
1. Click on the `POST /api/v1/generate-synthetic-network` endpoint
2. Click "Try it out"
3. Click "Execute"
4. View the response with the number of assets created

#### Option B: Command Line (curl)

From your host machine:


curl http://localhost:8000/api/v1/health
`bash
# Check if the API is running
curl http://localhost:8000/api/v1/health

# Generate synthetic network
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
```

#### Option C: Docker Exec (Inside Container)

This is what the user requested - running the generation from inside the container:

```bash
# Method 1: Using curl inside the container
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Method 2: Using the test script
docker exec udtcwafastapi bash /opt/udt/cwa/cwa_fastapi/test_api.sh
```

### 4. Verify the Data

Connect to the PostGIS database to verify the data was created:

```bash
docker exec -it udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_pipemain;"
docker exec -it udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_hydrant;"
docker exec -it udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_networkoptvalve;"
docker exec -it udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM waterpipes_pipeflow;"
```

### 5. Load to Neo4j (Optional)

To visualize the network as a graph, load it into Neo4j using the Django command:

```bash
docker-compose exec cwageodjango python3 manage.py load_network_to_neo4j
```

Then visit http://localhost:7474 and run a Cypher query:

```cypher
MATCH (n) RETURN n LIMIT 25
```

## API Endpoints

### Health Check
- **URL**: `GET /api/v1/health`
- **Description**: Check if the API is running
- **Example**:
  ```bash
  curl http://localhost:8000/api/v1/health
  ```
- **Response**:
  ```json
  {
    "status": "ok",
    "message": "FastAPI server is running"
  }
  ```

### Generate Synthetic Network
- **URL**: `POST /api/v1/generate-synthetic-network`
- **Description**: Generate a complete synthetic water network
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
  ```
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

## Troubleshooting

### Container Not Starting

Check the container logs:
```bash
docker-compose logs cwafastapi
```

### Database Connection Issues

Verify the PostGIS container is healthy:
```bash
docker-compose ps udtpostgis
```

### Port Already in Use

If port 8000 is already in use, you can change it in `docker-compose.yml`:
```yaml
cwafastapi:
  ports:
    - "8001:8000"  # Change 8001 to your preferred port
```

### Viewing Logs

```bash
# View FastAPI logs
docker-compose logs -f cwafastapi

# View all logs
docker-compose logs -f
```

## Comparing with Django Approach

### Django (Legacy)
```bash
docker-compose exec cwageodjango python3 manage.py generate_synthetic_network
```

### FastAPI (New)
```bash
# From host
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# From container
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
```

## Advantages of FastAPI Implementation

1. **API-First**: Built as a REST API from the ground up
2. **Interactive Docs**: Automatic Swagger UI and ReDoc documentation
3. **Easy Testing**: Test endpoints directly from the browser
4. **Modern**: Uses modern Python async features
5. **No Django Required**: Can run independently for API needs
6. **Better for Integration**: Easy to integrate with other services and front-ends

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Add more endpoints for your specific needs
- Integrate with frontend applications
- Add authentication if needed for production use

## Getting Help

- View the full documentation in the main README.md
- Check the FastAPI application README at `cwa/cwa_fastapi/README.md`
- Visit the interactive API docs at http://localhost:8000/docs
