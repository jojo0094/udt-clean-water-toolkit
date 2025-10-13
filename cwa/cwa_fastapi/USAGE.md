# FastAPI Usage Guide

## What You Asked For

> "I dont like django. can you migrate to fastpi approach. 
> at least, when I reun docker excec for generate_sytentif netowrk . thsi fastapi shodl work."

## ✅ DONE! Here's How It Works Now

### Before (Django - Old Way)
```bash
docker-compose exec cwageodjango python3 manage.py generate_synthetic_network
```

### After (FastAPI - New Way)
```bash
# Method 1: Docker exec with curl (exactly what you asked for!)
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Method 2: Direct from your host machine
curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Method 3: Interactive browser UI
# Just open: http://localhost:8000/docs
```

## Step-by-Step Usage

### 1. Start Everything
```bash
docker-compose up -d
```

### 2. Check FastAPI is Running
```bash
# Method A: Check health endpoint
curl http://localhost:8000/api/v1/health

# Method B: Check container logs
docker logs udtcwafastapi

# Method C: Open browser to http://localhost:8000
```

### 3. Generate Synthetic Network
```bash
# Using docker exec (as you requested!)
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network
```

**Expected Output:**
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

### 4. Verify Data Was Created
```bash
# Check how many pipes were created
docker exec udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_pipemain;"

# Check hydrants
docker exec udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_hydrant;"

# Check valves
docker exec udtpostgis psql -U postgis -d postgis -c "SELECT COUNT(*) FROM assets_networkoptvalve;"
```

## Why FastAPI is Better

1. **No Django Required** - Lightweight, focused on API
2. **Automatic Documentation** - Visit http://localhost:8000/docs
3. **Modern & Fast** - Uses latest Python async features
4. **Easy Testing** - Test in browser or with curl
5. **Works with Docker Exec** - Exactly what you wanted!

## Interactive API Documentation

FastAPI automatically creates beautiful API docs:

1. Open browser to: http://localhost:8000/docs
2. You'll see:
   - List of all endpoints
   - Try them directly in browser
   - See request/response formats
   - No Postman needed!

## All Available Endpoints

```
GET  /                                      - Welcome message
GET  /api/v1/health                         - Health check
POST /api/v1/generate-synthetic-network     - Generate network
GET  /docs                                  - Swagger UI (interactive)
GET  /redoc                                 - ReDoc (alternative docs)
```

## Common Commands

```bash
# Start services
docker-compose up -d

# View FastAPI logs
docker logs -f udtcwafastapi

# Generate network (the easy way!)
docker exec udtcwafastapi curl -X POST http://localhost:8000/api/v1/generate-synthetic-network

# Stop services
docker-compose down

# Rebuild FastAPI container
docker-compose build cwafastapi
docker-compose up -d cwafastapi
```

## Troubleshooting

### Port 8000 Already in Use?
Edit `docker-compose.yml`:
```yaml
cwafastapi:
  ports:
    - "8001:8000"  # Change to different port
```

### Container Not Starting?
```bash
# Check logs
docker logs udtcwafastapi

# Check if PostGIS is ready
docker-compose ps
```

### Can't Connect to Database?
```bash
# Verify PostGIS is healthy
docker exec udtpostgis pg_isready -U postgis
```

## Comparison Table

| Task | Django Way | FastAPI Way |
|------|-----------|-------------|
| Generate Network | `docker-compose exec cwageodjango python3 manage.py generate_synthetic_network` | `docker exec udtcwafastapi curl -X POST localhost:8000/api/v1/generate-synthetic-network` |
| Documentation | Manual | Automatic at /docs |
| Testing | Complex | Open browser |
| API Access | Not built-in | Native REST API |
| Performance | Good | Excellent |

## What's Next?

Now that you have FastAPI working:
1. Explore http://localhost:8000/docs
2. Build a frontend that calls the API
3. Add more endpoints for your needs
4. Integrate with other services

## Need Help?

- See QUICKSTART_FASTAPI.md for detailed guide
- See ARCHITECTURE.md for technical details
- See README.md in cwa/cwa_fastapi/ for more info
- Visit http://localhost:8000/docs for API reference
