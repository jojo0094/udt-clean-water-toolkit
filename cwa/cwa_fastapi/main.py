from fastapi import FastAPI
from routes import router
from database import engine, Base

app = FastAPI(
    title="Clean Water Analytics API",
    description="FastAPI application for water network analysis and synthetic data generation",
    version="1.0.0"
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["water-network"])

@app.get("/")
def root():
    return {
        "message": "Clean Water Analytics FastAPI",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
