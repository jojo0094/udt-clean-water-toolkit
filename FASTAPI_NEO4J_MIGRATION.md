# FastAPI Neo4j Migration - Django Dependency Removal

## Overview

This document describes the migration of the `load_network_to_neo4j` functionality from Django to FastAPI, removing Django dependencies for this critical feature.

## What Was Done

### 1. SQLAlchemy Model Enhancements
Added compatibility layer to SQLAlchemy models to work with existing GisToGraph code:
- Added `pk` property to models (maps to `id`)
- Added `AssetMeta` inner class with `asset_name` attribute
- Models affected: `PipeMain`, `Hydrant`, `NetworkOptValve`

### 2. GisToNeo4j Adapter
Created `gis_to_neo4j_adapter.py` - a compatibility layer that:
- Extends the cleanwater `GisToNeo4j` class
- Overrides Django-specific methods to work with SQLAlchemy/GeoAlchemy2
- Handles geometry conversion between GeoAlchemy2 and Shapely
- Implements spatial queries using PostGIS functions

### 3. FastAPI Endpoints

#### POST /api/v1/load-to-neo4j
Loads water network data from PostGIS into Neo4j graph database.

**Features:**
- Clears existing Neo4j data
- Loads pipes with spatial relationships
- Includes point assets (hydrants, valves)
- Eager loads relationships for performance

**Example:**
```bash
curl -X POST http://localhost:8000/api/v1/load-to-neo4j
```

**Response:**
```json
{
  "status": "success",
  "message": "Successfully loaded network into Neo4j",
  "pipes_loaded": 22
}
```

#### GET /api/v1/verify-neo4j
Verifies that data exists in Neo4j database.

**Example:**
```bash
curl http://localhost:8000/api/v1/verify-neo4j
```

**Response:**
```json
{
  "status": "success",
  "message": "Neo4j database contains data",
  "node_count": 125,
  "relationship_count": 200
}
```

### 4. Configuration Validation
Created `config_validator.py` - a Pydantic-based configuration validator:
- Replaces Django forms with Pydantic models
- Provides same validation as Django version
- No Django dependencies
- Type-safe with better error messages

### 5. Dependencies Added
Updated `requirements.txt` with:
- `neomodel==5.2.1` - Neo4j ORM
- `neo4j==5.15.0` - Neo4j driver
- `sqids==0.4.1` - ID encoding
- `annotated-types==0.7.0` - Type annotations

### 6. Neo4j Configuration
Enhanced `database.py` to configure neomodel:
- Reads Neo4j connection settings from environment variables
- Auto-configures neomodel on import
- Falls back gracefully if neomodel not installed

## Complete Workflow

### Step 1: Generate Synthetic Network
```bash
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
```

This creates:
- Pipes in PostGIS
- Hydrants at pipe intersections
- Valves at pipe junctions
- Flow data for each pipe

### Step 2: Load to Neo4j
```bash
curl -X POST http://localhost:8000/api/v1/load-to-neo4j
```

This:
- Clears existing Neo4j data
- Transforms PostGIS geometries to graph nodes
- Creates relationships between network elements
- Preserves DMA and utility associations

### Step 3: Verify Neo4j
```bash
curl http://localhost:8000/api/v1/verify-neo4j
```

Confirms:
- Nodes were created
- Relationships were established
- Data is queryable

### Step 4: Explore in Neo4j Browser
Open http://localhost:7474 and run:
```cypher
MATCH (n) RETURN n LIMIT 25
```

## Technical Details

### Geometry Conversion
The adapter handles conversion between three geometry representations:
1. **GeoAlchemy2 WKBElement**: Database storage format
2. **Shapely Geometry**: Python geometric operations
3. **WKT String**: Text representation for Neo4j

### Spatial Queries
Uses PostGIS ST_Intersects for finding assets along pipes:
```python
ST_Intersects(model.geometry, pipe_geom)
```

### Lazy Loading Prevention
Uses SQLAlchemy `joinedload` to prevent N+1 queries:
```python
db.query(PipeMain).options(
    joinedload(PipeMain.dmas).joinedload(DMA.utility)
).all()
```

## Comparison: Django vs FastAPI

### Before (Django)
```bash
# Required Django ORM and GeoDjango
docker-compose exec cwageodjango python3 manage.py load_network_to_neo4j

# Limitations:
# - Django framework required
# - CLI-only interface
# - Tightly coupled to Django models
```

### After (FastAPI)
```bash
# Pure REST API, no Django required
curl -X POST http://localhost:8000/api/v1/load-to-neo4j

# Benefits:
# - No Django dependency for this feature
# - RESTful API interface
# - SQLAlchemy compatibility layer
# - Works with any HTTP client
# - Can be called from other services
```

## Files Changed/Created

### New Files
- `cwa/cwa_fastapi/gis_to_neo4j_adapter.py` - SQLAlchemy adapter
- `cwa/cwa_fastapi/config_validator.py` - Pydantic config validator
- `FASTAPI_NEO4J_MIGRATION.md` - This documentation

### Modified Files
- `cwa/cwa_fastapi/models.py` - Added pk property and AssetMeta
- `cwa/cwa_fastapi/routes.py` - Added load-to-neo4j and verify-neo4j endpoints
- `cwa/cwa_fastapi/database.py` - Added Neo4j configuration
- `cwa/cwa_fastapi/requirements.txt` - Added neomodel, neo4j, sqids
- `cwa/cwa_fastapi/README.md` - Updated documentation
- `cwa/cwa_fastapi/test_api.sh` - Added new endpoint tests
- `MIGRATION_SUMMARY.md` - Updated with new endpoints

## Environment Variables

Ensure these are set in your `.env` file:

```bash
# Neo4j Configuration
CWA_NEO4J_HOST=bolt://udtneo4j
CWA_NEO4J_PORT=7687
CWA_NEO4J_USER=neo4j
CWA_NEO4J_PASSWORD=your_password

# PostGIS Configuration (existing)
POSTGIS_DB_NAME__ENV_VAR=postgis
POSTGIS_DB_USER__ENV_VAR=postgis
POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR=postgis
POSTGIS_DEFAULT_DB_HOST__ENV_VAR=udtpostgis
POSTGIS_DEFAULT_PORT__ENV_VAR=5432
```

## Testing

### Unit Test
```python
# Test adapter directly
from gis_to_neo4j_adapter import GisToNeo4jAdapter
adapter = GisToNeo4jAdapter(srid=27700, sqids=sqids, db_session=db)
```

### Integration Test
```bash
# Run the complete workflow
bash /opt/udt/cwa/cwa_fastapi/test_api.sh
```

### Manual Test
1. Generate network
2. Load to Neo4j
3. Verify in Neo4j Browser
4. Run Cypher queries

## Known Limitations

1. **Pipe Junctions**: Currently returns empty list (handled by intersections)
2. **Pre-fetched Data**: Some Django-specific prefetch optimizations not ported
3. **Geometry Types**: Only handles LINESTRING pipes and POINT assets

## Future Improvements

1. **Async Support**: Make Neo4j loading async for better performance
2. **Batch Processing**: Add batch size configuration for large datasets
3. **Progress Tracking**: WebSocket updates during loading
4. **Validation**: Pre-validate geometry before loading
5. **Rollback**: Transaction support for failed loads

## Troubleshooting

### Neo4j Connection Error
```
Error: Could not connect to Neo4j
```
**Solution**: Check Neo4j container is running and credentials are correct

### Geometry Conversion Error
```
Error: Cannot convert geometry to WKT
```
**Solution**: Ensure GeoAlchemy2 and Shapely are installed

### Missing Assets
```
Warning: No point assets found
```
**Solution**: Generate synthetic network first, then load to Neo4j

### Import Error
```
ImportError: No module named 'neomodel'
```
**Solution**: Install requirements: `pip install -r requirements.txt`

## Summary

✅ **Django dependency removed for Neo4j loading**  
✅ **FastAPI REST API for network loading**  
✅ **SQLAlchemy/GeoAlchemy2 compatibility layer**  
✅ **Pydantic-based configuration validation**  
✅ **Complete workflow documentation**  
✅ **Backward compatible with existing Neo4j queries**  

The load-to-neo4j functionality is now available as a REST API endpoint without requiring Django!
