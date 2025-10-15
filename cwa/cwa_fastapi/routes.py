import random
import json
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from geoalchemy2.elements import WKTElement
from database import get_db
from models import Utility, DMA, PipeMain, Hydrant, NetworkOptValve, PipeFlow
from schemas import GenerateSyntheticNetworkResponse, HealthCheckResponse
#path append
import sys
sys.path.append('/opt/udt/')

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
        # BNG coordinates for London area
        min_x_bng, min_y_bng = 529000, 181000
        max_x_bng, max_y_bng = 530000, 182000
        # WGS84 coordinates for geometry_4326 fields
        min_x_wgs, min_y_wgs = -0.1, 51.5
        max_x_wgs, max_y_wgs = -0.09, 51.51
        grid_size = 10  # 10x10 grid

        # 3. Create a utility and a DMA
        utility = Utility(name="synthetic_utility")
        db.add(utility)
        db.flush()

        # Create a polygon for the DMA's geometry using WKT
        # Note: Using SRID 27700 for British National Grid (matching model)
        # Convert coordinates to approximate BNG values
        min_x_bng, min_y_bng = 529000, 181000  # Approximate BNG for London area
        max_x_bng, max_y_bng = 530000, 182000
        dma_wkt = f"MULTIPOLYGON((({min_x_bng} {min_y_bng},{max_x_bng} {min_y_bng},{max_x_bng} {max_y_bng},{min_x_bng} {max_y_bng},{min_x_bng} {min_y_bng})))"
        
        dma = DMA(
            code="SYNTHETIC_DMA_01",
            name="Synthetic DMA 01",
            utility_id=utility.id,
            geometry=WKTElement(dma_wkt, srid=27700)
        )
        db.add(dma)
        db.flush()

        # 4. Generate a street grid and create PipeMain objects
        pipe_mains = []
        
        # Horizontal pipes
        for i in range(grid_size + 1):
            y_bng = min_y_bng + (i * (max_y_bng - min_y_bng) / grid_size)
            y_wgs = min_y_wgs + (i * (max_y_wgs - min_y_wgs) / grid_size)
            line_wkt_bng = f"LINESTRING({min_x_bng} {y_bng},{max_x_bng} {y_bng})"
            line_wkt_wgs = f"LINESTRING({min_x_wgs} {y_wgs},{max_x_wgs} {y_wgs})"
            pipe = PipeMain(
                tag=f"H_PIPE_{i}",
                geometry=WKTElement(line_wkt_bng, srid=27700),
                geometry_4326=WKTElement(line_wkt_wgs, srid=4326),
                material=random.choice(['Iron', 'PVC', 'Copper']),
                diameter=random.choice([100, 150, 200, 250, 300]),
                pipe_type='Distribution Main'
            )
            pipe_mains.append(pipe)

        # Vertical pipes
        for i in range(grid_size + 1):
            x_bng = min_x_bng + (i * (max_x_bng - min_x_bng) / grid_size)
            x_wgs = min_x_wgs + (i * (max_x_wgs - min_x_wgs) / grid_size)
            line_wkt_bng = f"LINESTRING({x_bng} {min_y_bng},{x_bng} {max_y_bng})"
            line_wkt_wgs = f"LINESTRING({x_wgs} {min_y_wgs},{x_wgs} {max_y_wgs})"
            pipe = PipeMain(
                tag=f"V_PIPE_{i}",
                geometry=WKTElement(line_wkt_bng, srid=27700),
                geometry_4326=WKTElement(line_wkt_wgs, srid=4326),
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
            # Add a hydrant somewhere along the pipe (50% chance)
            if random.random() > 0.5:
                # Get the start and end points of the pipe
                tag = pipe.tag
                if tag.startswith("H_PIPE_"):
                    # Horizontal pipe
                    i = int(tag.replace("H_PIPE_", ""))
                    y_bng = min_y_bng + (i * (max_y_bng - min_y_bng) / grid_size)
                    y_wgs = min_y_wgs + (i * (max_y_wgs - min_y_wgs) / grid_size)
                    t = random.random()
                    x_bng = min_x_bng + t * (max_x_bng - min_x_bng)
                    x_wgs = min_x_wgs + t * (max_x_wgs - min_x_wgs)
                    point_wkt_bng = f"POINT({x_bng} {y_bng})"
                    point_wkt_wgs = f"POINT({x_wgs} {y_wgs})"
                elif tag.startswith("V_PIPE_"):
                    # Vertical pipe
                    i = int(tag.replace("V_PIPE_", ""))
                    x_bng = min_x_bng + (i * (max_x_bng - min_x_bng) / grid_size)
                    x_wgs = min_x_wgs + (i * (max_x_wgs - min_x_wgs) / grid_size)
                    t = random.random()
                    y_bng = min_y_bng + t * (max_y_bng - min_y_bng)
                    y_wgs = min_y_wgs + t * (max_y_wgs - min_y_wgs)
                    point_wkt_bng = f"POINT({x_bng} {y_bng})"
                    point_wkt_wgs = f"POINT({x_wgs} {y_wgs})"
                else:
                    continue
                
                hydrant = Hydrant(
                    tag=f"HYD_{pipe.tag}",
                    geometry=WKTElement(point_wkt_bng, srid=27700),
                    geometry_4326=WKTElement(point_wkt_wgs, srid=4326),
                    acoustic_logger=random.choice([True, False])
                )
                hydrants.append(hydrant)

            # Add a valve somewhere along the pipe (30% chance)
            if random.random() > 0.7:
                tag = pipe.tag
                if tag.startswith("H_PIPE_"):
                    i = int(tag.replace("H_PIPE_", ""))
                    y_bng = min_y_bng + (i * (max_y_bng - min_y_bng) / grid_size)
                    y_wgs = min_y_wgs + (i * (max_y_wgs - min_y_wgs) / grid_size)
                    t = random.random()
                    x_bng = min_x_bng + t * (max_x_bng - min_x_bng)
                    x_wgs = min_x_wgs + t * (max_x_wgs - min_x_wgs)
                    point_wkt_bng = f"POINT({x_bng} {y_bng})"
                    point_wkt_wgs = f"POINT({x_wgs} {y_wgs})"
                elif tag.startswith("V_PIPE_"):
                    i = int(tag.replace("V_PIPE_", ""))
                    x_bng = min_x_bng + (i * (max_x_bng - min_x_bng) / grid_size)
                    x_wgs = min_x_wgs + (i * (max_x_wgs - min_x_wgs) / grid_size)
                    t = random.random()
                    y_bng = min_y_bng + t * (max_y_bng - min_y_bng)
                    y_wgs = min_y_wgs + t * (max_y_wgs - min_y_wgs)
                    point_wkt_bng = f"POINT({x_bng} {y_bng})"
                    point_wkt_wgs = f"POINT({x_wgs} {y_wgs})"
                else:
                    continue
                    
                valve = NetworkOptValve(
                    tag=f"VALVE_{pipe.tag}",
                    geometry=WKTElement(point_wkt_bng, srid=27700),
                    geometry_4326=WKTElement(point_wkt_wgs, srid=4326),
                    acoustic_logger=random.choice([True, False])
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

@router.post("/load-to-neo4j", response_model=dict)
def load_to_neo4j(db: Session = Depends(get_db)):
    """
    Load the synthetic network from PostGIS into Neo4j.
    Transforms point assets (hydrants, valves) and pipe relationships.
    
    This endpoint uses the GisToNeo4jAdapter which provides compatibility
    between SQLAlchemy/GeoAlchemy2 and the cleanwater GisToNeo4j transformer.
    """
    try:
        from neomodel import db as neo4j_db
        from gis_to_neo4j_adapter import GisToNeo4jAdapter
        from constants import (
            HYDRANT__NAME,
            NETWORK_OPT_VALVE__NAME,
            DEFAULT_SRID,
        )
        from sqids import Sqids

        # 1. Clear Neo4j database
        neo4j_db.cypher_query("MATCH (n) DETACH DELETE n")

        # 2. Define point assets to include
        point_asset_names = [
            HYDRANT__NAME,
            NETWORK_OPT_VALVE__NAME,
        ]

        # 3. Initialize transformation with SQLAlchemy-compatible adapter
        sqids = Sqids()
        gis_to_neo4j = GisToNeo4jAdapter(
            srid=DEFAULT_SRID,
            sqids=sqids,
            point_asset_names=point_asset_names,
            db_session=db,  # Pass SQLAlchemy session
        )

        # 4. Get all pipes from PostGIS with eager loading of relationships
        # Eager load relationships to avoid lazy loading issues
        pipes = db.query(PipeMain).options(
            joinedload(PipeMain.dmas).joinedload(DMA.utility)
        ).all()
        
        if not pipes:
            raise Exception("No pipes found in PostGIS database")

        # 5. Calculate graph components
        gis_to_neo4j.calc_pipe_point_relative_positions(pipes)

        # 6. Create Neo4j graph
        gis_to_neo4j.create_neo4j_graph()

        return {
            "status": "success",
            "message": "Successfully loaded network into Neo4j",
            "pipes_loaded": len(pipes),
        }

    except Exception as e:
        import traceback
        error_detail = f"Error loading to Neo4j: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@router.get("/verify-neo4j", response_model=dict)
def verify_neo4j():
    """
    Verify that data has been loaded into the Neo4j database.
    Returns counts of nodes and relationships.
    """
    try:
        from neomodel import db as neo4j_db
        
        # Query to count nodes
        node_results, _ = neo4j_db.cypher_query("MATCH (n) RETURN count(n) AS node_count")
        node_count = node_results[0][0] if node_results else 0
        
        # Query to count relationships
        rel_results, _ = neo4j_db.cypher_query("MATCH ()-[r]->() RETURN count(r) AS rel_count")
        rel_count = rel_results[0][0] if rel_results else 0
        
        if node_count > 0 and rel_count > 0:
            return {
                "status": "success",
                "message": "Neo4j database contains data",
                "node_count": node_count,
                "relationship_count": rel_count
            }
        else:
            return {
                "status": "warning",
                "message": "Neo4j database is empty or partially loaded",
                "node_count": node_count,
                "relationship_count": rel_count
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying Neo4j: {str(e)}")
def generate_random_flow_data_dict():
    """Generate random flow data for 24 hours at 15-minute intervals"""
    start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    flow_data = {}

    for i in range(0, 24 * 4):  # 24 hours * 4 (15-minute intervals per hour)
        time_slot = start_time + timedelta(minutes=i * 15)
        flow_value = round(random.uniform(0.0, 100.0), 2)
        flow_data[time_slot.isoformat()] = flow_value

    return flow_data
