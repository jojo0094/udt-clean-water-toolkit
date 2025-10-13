import random
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import LineString, Point, Polygon, MultiPolygon as ShapelyMultiPolygon
from .database import get_db
from .models import Utility, DMA, PipeMain, Hydrant, NetworkOptValve, PipeFlow
from .schemas import GenerateSyntheticNetworkResponse, HealthCheckResponse

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "FastAPI server is running"}

@router.post("/generate-synthetic-network", response_model=GenerateSyntheticNetworkResponse)
def generate_synthetic_network(db: Session = Depends(get_db)):
    """
    Generate a synthetic water network for demonstration purposes.
    This endpoint creates pipes, hydrants, valves, and flow data.
    """
    try:
        # 1. Clean up any existing data
        db.query(PipeFlow).delete()
        db.query(Hydrant).delete()
        db.query(NetworkOptValve).delete()
        db.query(PipeMain).delete()
        db.query(DMA).delete()
        db.query(Utility).delete()
        db.commit()

        # 2. Define a geographic area (a simple 1km x 1km grid)
        min_x, min_y = -0.1, 51.5
        max_x, max_y = -0.09, 51.51
        grid_size = 10  # 10x10 grid

        # 3. Create a utility and a DMA
        utility = Utility(name="synthetic_utility")
        db.add(utility)
        db.flush()

        # Create a polygon for the DMA's geometry
        dma_polygon = Polygon([(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y), (min_x, min_y)])
        dma_multipolygon = ShapelyMultiPolygon([dma_polygon])
        
        dma = DMA(
            code="SYNTHETIC_DMA_01",
            name="Synthetic DMA 01",
            utility_id=utility.id,
            geometry=from_shape(dma_multipolygon, srid=4326)
        )
        db.add(dma)
        db.flush()

        # 4. Generate a street grid and create PipeMain objects
        pipe_mains = []
        
        # Horizontal pipes
        for i in range(grid_size + 1):
            y = min_y + (i * (max_y - min_y) / grid_size)
            line = LineString([(min_x, y), (max_x, y)])
            pipe = PipeMain(
                tag=f"H_PIPE_{i}",
                geometry=from_shape(line, srid=4326),
                geometry_4326=from_shape(line, srid=4326),
                material=random.choice(['Iron', 'PVC', 'Copper']),
                diameter=random.choice([100, 150, 200, 250, 300]),
                pipe_type='Distribution Main'
            )
            pipe_mains.append(pipe)

        # Vertical pipes
        for i in range(grid_size + 1):
            x = min_x + (i * (max_x - min_x) / grid_size)
            line = LineString([(x, min_y), (x, max_y)])
            pipe = PipeMain(
                tag=f"V_PIPE_{i}",
                geometry=from_shape(line, srid=4326),
                geometry_4326=from_shape(line, srid=4326),
                material=random.choice(['Iron', 'PVC', 'Copper']),
                diameter=random.choice([100, 150, 200, 250, 300]),
                pipe_type='Distribution Main'
            )
            pipe_mains.append(pipe)

        db.add_all(pipe_mains)
        db.flush()

        # Add all pipes to the DMA
        for pipe in pipe_mains:
            pipe.dmas.append(dma)

        # 5. Generate assets along the pipes
        hydrants = []
        valves = []
        
        for pipe in pipe_mains:
            # Add a hydrant somewhere along the pipe
            if random.random() > 0.5:  # 50% chance
                # Simple interpolation for point generation
                t = random.random()
                coords = list(pipe.geometry.coords) if hasattr(pipe.geometry, 'coords') else None
                if coords and len(coords) >= 2:
                    x = coords[0][0] + t * (coords[1][0] - coords[0][0])
                    y = coords[0][1] + t * (coords[1][1] - coords[0][1])
                    point = Point(x, y)
                    hydrant = Hydrant(
                        tag=f"HYD_{pipe.tag}",
                        geometry=from_shape(point, srid=4326),
                        geometry_4326=from_shape(point, srid=4326),
                        acoustic_logger=str(random.choice([True, False]))
                    )
                    hydrants.append(hydrant)

            # Add a valve somewhere along the pipe
            if random.random() > 0.7:  # 30% chance
                t = random.random()
                coords = list(pipe.geometry.coords) if hasattr(pipe.geometry, 'coords') else None
                if coords and len(coords) >= 2:
                    x = coords[0][0] + t * (coords[1][0] - coords[0][0])
                    y = coords[0][1] + t * (coords[1][1] - coords[0][1])
                    point = Point(x, y)
                    valve = NetworkOptValve(
                        tag=f"VALVE_{pipe.tag}",
                        geometry=from_shape(point, srid=4326),
                        geometry_4326=from_shape(point, srid=4326),
                        acoustic_logger=str(random.choice([True, False]))
                    )
                    valves.append(valve)

        db.add_all(hydrants)
        db.add_all(valves)
        db.flush()

        # Add hydrants and valves to DMA
        for hydrant in hydrants:
            hydrant.dmas.append(dma)
        for valve in valves:
            valve.dmas.append(dma)

        # 6. Generate flow data for the new pipes
        pipe_flows = []
        for pipe in pipe_mains:
            flow_data = generate_random_flow_data_dict()
            pipe_flow = PipeFlow(
                pipe_main_id=pipe.id,
                flow_data=flow_data
            )
            pipe_flows.append(pipe_flow)

        db.add_all(pipe_flows)
        db.commit()

        return {
            "status": "success",
            "message": "Successfully generated synthetic network",
            "pipes_created": len(pipe_mains),
            "hydrants_created": len(hydrants),
            "valves_created": len(valves),
            "flow_records_created": len(pipe_flows)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating synthetic network: {str(e)}")

def generate_random_flow_data_dict():
    """Generate random flow data for 24 hours at 15-minute intervals"""
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    flow_data = {}

    for i in range(0, 24 * 4):  # 24 hours * 4 (15-minute intervals per hour)
        time_slot = start_time + timedelta(minutes=i * 15)
        flow_value = round(random.uniform(0.0, 100.0), 2)
        flow_data[time_slot.isoformat()] = flow_value

    return flow_data
