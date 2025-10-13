# Quick Start: Generate Network and Load to Neo4j

This guide shows you how to generate a synthetic water network and load it into Neo4j using the new FastAPI endpoints (no Django required!).

## Prerequisites

- Docker and Docker Compose installed
- Configured `.env` file with database credentials

## Step-by-Step Guide

### 1. Start All Services

```bash
docker-compose up -d
```

This starts:
- PostGIS (database for spatial data)
- Neo4j (graph database)
- FastAPI (REST API server)

### 2. Check API is Running

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{"status": "ok", "message": "FastAPI server is running"}
```

### 3. Generate Synthetic Network

```bash
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
```

Expected response:
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

This creates a 10x10 grid of water pipes with hydrants and valves in PostGIS.

### 4. Load Network to Neo4j

```bash
curl -X POST http://localhost:8000/api/v1/load-to-neo4j
```

Expected response:
```json
{
  "status": "success",
  "message": "Successfully loaded network into Neo4j",
  "pipes_loaded": 22
}
```

This transforms the PostGIS spatial data into a Neo4j graph with nodes and relationships.

### 5. Verify Neo4j Data

```bash
curl http://localhost:8000/api/v1/verify-neo4j
```

Expected response:
```json
{
  "status": "success",
  "message": "Neo4j database contains data",
  "node_count": 125,
  "relationship_count": 200
}
```

### 6. Explore in Neo4j Browser

Open Neo4j Browser: http://localhost:7474

Default credentials:
- Username: `neo4j`
- Password: (check your `.env` file - `CWA_NEO4J_PASSWORD`)

Run this query to see the graph:
```cypher
MATCH (n) RETURN n LIMIT 25
```

## Using Docker Exec (Alternative Method)

If you prefer to run commands from inside the container:

```bash
# Generate network
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Load to Neo4j
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/load-to-neo4j

# Verify
docker exec udtcwafastapi curl http://localhost:8000/api/v1/verify-neo4j
```

## Using the Test Script

A test script is provided that runs all commands:

```bash
docker exec udtcwafastapi bash /opt/udt/cwa/cwa_fastapi/test_api.sh
```

## Interactive API Documentation

For interactive testing, open your browser to:

**Swagger UI**: http://localhost:8000/docs

Here you can:
1. See all available endpoints
2. Try them out directly in the browser
3. View request/response schemas
4. Test with different parameters

## Troubleshooting

### Connection Refused
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Solution**: Wait a few seconds for FastAPI to start, then try again.

### No Pipes Found
```
{"detail": "Error loading to Neo4j: No pipes found in PostGIS database"}
```

**Solution**: Run generate-synthetic-network first.

### Neo4j Connection Error
```
{"detail": "Error loading to Neo4j: Could not connect to Neo4j"}
```

**Solution**: Check that Neo4j container is running:
```bash
docker-compose ps udtneo4j
```

### Empty Neo4j Database
```
{"status": "warning", "node_count": 0, "relationship_count": 0}
```

**Solution**: Run load-to-neo4j endpoint first.

## What Gets Created?

### PostGIS Tables
- `assets_pipemain` - Water pipes (22 pipes in 10x10 grid)
- `assets_hydrant` - Fire hydrants (~11 hydrants)
- `assets_networkoptvalve` - Network valves (~7 valves)
- `utilities_utility` - Water utility company (1 record)
- `utilities_dma` - District Metered Area (1 DMA)
- `waterpipes_pipeflow` - Flow data (22 records with time-series data)

### Neo4j Graph
- **Nodes**: Pipe junctions, pipe ends, hydrants, valves
- **Relationships**: Pipe connections, asset associations
- **Properties**: Coordinates, pipe material, diameter, DMA codes

## Example Neo4j Queries

### Count All Nodes
```cypher
MATCH (n) RETURN count(n) AS node_count
```

### Count All Relationships
```cypher
MATCH ()-[r]->() RETURN count(r) AS rel_count
```

### Find All Pipe Nodes
```cypher
MATCH (n:PipeNode) RETURN n LIMIT 10
```

### Find All Point Assets
```cypher
MATCH (n:PointAsset) RETURN n LIMIT 10
```

### Find Connected Nodes
```cypher
MATCH (n)-[r]-(m) RETURN n, r, m LIMIT 50
```

## Complete Workflow in One Script

Create a file `run_workflow.sh`:

```bash
#!/bin/bash
set -e

echo "1. Checking API health..."
curl -s http://localhost:8000/api/v1/health | jq

echo -e "\n2. Generating synthetic network..."
curl -s -X POST http://localhost:8000/api/v1/generate-synthetic-network | jq

echo -e "\n3. Loading to Neo4j..."
curl -s -X POST http://localhost:8000/api/v1/load-to-neo4j | jq

echo -e "\n4. Verifying Neo4j data..."
curl -s http://localhost:8000/api/v1/verify-neo4j | jq

echo -e "\n✅ Complete! Visit http://localhost:7474 to explore the graph."
```

Make it executable and run:
```bash
chmod +x run_workflow.sh
./run_workflow.sh
```

## Next Steps

After loading data to Neo4j, you can:

1. **Visualize the network** in Neo4j Browser
2. **Run analysis queries** to find patterns
3. **Calculate network metrics** like betweenness centrality
4. **Export to other formats** using Neo4j export tools
5. **Integrate with other tools** that support Neo4j

## Need Help?

- **API Documentation**: http://localhost:8000/docs
- **FastAPI README**: `cwa/cwa_fastapi/README.md`
- **Technical Details**: `FASTAPI_NEO4J_MIGRATION.md`
- **Django Removal**: `DJANGO_REMOVAL_SUMMARY.md`

## Summary

You now have a complete workflow to:
1. ✅ Generate synthetic water networks via API
2. ✅ Load spatial data to Neo4j graph database
3. ✅ Verify and explore the graph
4. ✅ All without Django dependency!

Happy graphing! 🎉
