# FastAPI Application Architecture

## Overview

The FastAPI application provides a REST API for water network operations, built with modern Python frameworks and optimized for performance.

## Technology Stack

```
┌─────────────────────────────────────────┐
│         FastAPI Application             │
│  (Async web framework with auto docs)   │
└────────────┬────────────────────────────┘
             │
             ├─── Routes (routes.py)
             │    └─── Business logic for endpoints
             │
             ├─── Schemas (schemas.py)
             │    └─── Pydantic models for validation
             │
             ├─── Models (models.py)
             │    └─── SQLAlchemy ORM models
             │
             └─── Database (database.py)
                  └─── Connection management
                       │
                       ▼
             ┌─────────────────────┐
             │   PostGIS Database  │
             │   (PostgreSQL +     │
             │    Spatial Ext.)    │
             └─────────────────────┘
```

## Components

### 1. Main Application (`main.py`)
- FastAPI app initialization
- Router registration
- Serves interactive documentation

### 2. Routes (`routes.py`)
- `/api/v1/health` - Health check endpoint
- `/api/v1/generate-synthetic-network` - Network generation endpoint
- Business logic for synthetic data generation

### 3. Models (`models.py`)
SQLAlchemy ORM models for:
- `Utility` - Water utility organizations
- `DMA` - District Metered Areas
- `PipeMain` - Water pipes (LineString geometry)
- `Hydrant` - Fire hydrants (Point geometry)
- `NetworkOptValve` - Network valves (Point geometry)
- `PipeFlow` - Time-series flow data (JSON)

### 4. Schemas (`schemas.py`)
Pydantic models for:
- Request validation
- Response formatting
- API documentation

### 5. Database (`database.py`)
- Database connection configuration
- Session management
- Connection pooling

## Data Flow: Generate Synthetic Network

```
HTTP POST Request
      │
      ▼
┌──────────────────┐
│ FastAPI Endpoint │
│  (routes.py)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ 1. Clean existing data   │
│    - Delete old records  │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ 2. Create Utility & DMA  │
│    - Organization setup  │
│    - Geographic bounds   │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ 3. Generate Pipe Grid    │
│    - 10x10 grid pattern  │
│    - Horizontal pipes    │
│    - Vertical pipes      │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ 4. Add Point Assets      │
│    - Hydrants (50%)      │
│    - Valves (30%)        │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ 5. Generate Flow Data    │
│    - 24hr @ 15min        │
│    - Random values       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ 6. Commit to Database    │
└────────┬─────────────────┘
         │
         ▼
    JSON Response
```

## Geometry Handling

The application uses **GeoAlchemy2** for spatial data:

```python
from geoalchemy2.elements import WKTElement

# Create a line geometry
line_wkt = f"LINESTRING({x1} {y1},{x2} {y2})"
geometry = WKTElement(line_wkt, srid=4326)

# Create a point geometry
point_wkt = f"POINT({x} {y})"
geometry = WKTElement(point_wkt, srid=4326)
```

**SRID 4326** = WGS84 (GPS coordinates - latitude/longitude)

## Database Tables

```
utilities_utility
├─ id (PK)
├─ name
└─ timestamps

utilities_dma
├─ id (PK)
├─ code
├─ name
├─ utility_id (FK)
├─ geometry (MultiPolygon)
└─ timestamps

assets_pipemain
├─ id (PK)
├─ tag (unique)
├─ geometry (LineString)
├─ geometry_4326 (LineString)
├─ material
├─ diameter
├─ pipe_type
└─ timestamps

assets_hydrant
├─ id (PK)
├─ tag (unique)
├─ geometry (Point)
├─ geometry_4326 (Point)
├─ acoustic_logger
└─ timestamps

assets_networkoptvalve
├─ id (PK)
├─ tag (unique)
├─ geometry (Point)
├─ geometry_4326 (Point)
├─ acoustic_logger
└─ timestamps

waterpipes_pipeflow
├─ pipe_main_id (PK, FK)
└─ flow_data (JSON)
```

## API Documentation

FastAPI automatically generates:
- **OpenAPI (Swagger)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Deployment

### Docker Container
- Base: Ubuntu 22.04
- Python: 3.11
- GDAL: For spatial operations
- Uvicorn: ASGI server with auto-reload
- Port: 8000

### Environment Variables
```bash
POSTGIS_DB_NAME__ENV_VAR=postgis
POSTGIS_DB_USER__ENV_VAR=postgis
POSTGIS_DEFAULT_DB_HOST__ENV_VAR=udtpostgis
POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR=postgis
POSTGIS_DEFAULT_PORT__ENV_VAR=5432
```

## Future Enhancements

Potential additions:
1. **Authentication**: JWT tokens for secure API access
2. **More Endpoints**: 
   - List networks
   - Query specific assets
   - Update network data
   - Delete networks
3. **Async Operations**: Long-running tasks with background workers
4. **WebSocket Support**: Real-time updates
5. **Rate Limiting**: API request throttling
6. **Caching**: Redis for frequently accessed data
7. **Metrics**: Prometheus/monitoring integration

## Performance Considerations

- **Bulk Operations**: Uses `bulk_create` for efficiency
- **Connection Pooling**: SQLAlchemy manages connections
- **Async Ready**: FastAPI supports async operations
- **Lazy Loading**: Relationships loaded on demand

## Testing

```bash
# Verify setup
cd cwa/cwa_fastapi
python3 verify_setup.py

# Run tests
pytest tests/

# Manual testing
./test_api.sh
```

## Comparison: Django vs FastAPI

| Feature | Django | FastAPI |
|---------|--------|---------|
| Type | Full framework | Micro framework |
| Admin UI | ✅ Built-in | ❌ None |
| ORM | Django ORM | SQLAlchemy |
| API Docs | ❌ Manual | ✅ Automatic |
| Performance | Good | Excellent |
| Async | Limited | Full support |
| Learning Curve | Moderate | Easy |
| Use Case | Full web apps | APIs |

## Related Files

- `/cwa/cwa_fastapi/` - FastAPI application
- `/cwa/cwa_geodjango/` - Django application (legacy)
- `/docker-compose.yml` - Container orchestration
- `/devops/docker/Dockerfile_cwa_fastapi` - FastAPI container
