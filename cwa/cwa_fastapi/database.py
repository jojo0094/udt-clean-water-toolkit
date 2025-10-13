import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL/PostGIS Database connection configuration
POSTGIS_DB_NAME = os.getenv("POSTGIS_DB_NAME__ENV_VAR", "postgis")
POSTGIS_DB_USER = os.getenv("POSTGIS_DB_USER__ENV_VAR", "postgis")
POSTGIS_DB_PASSWORD = os.getenv("POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR", "postgis")
POSTGIS_DB_HOST = os.getenv("POSTGIS_DEFAULT_DB_HOST__ENV_VAR", "udtpostgis")
POSTGIS_DB_PORT = os.getenv("POSTGIS_DEFAULT_PORT__ENV_VAR", "5432")

DATABASE_URL = f"postgresql://{POSTGIS_DB_USER}:{POSTGIS_DB_PASSWORD}@{POSTGIS_DB_HOST}:{POSTGIS_DB_PORT}/{POSTGIS_DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Neo4j configuration for neomodel
NEO4J_HOST = os.getenv("CWA_NEO4J_HOST", "bolt://udtneo4j")
NEO4J_PORT = os.getenv("CWA_NEO4J_PORT", "7687")
NEO4J_USER = os.getenv("CWA_NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("CWA_NEO4J_PASSWORD", "password")

# Configure neomodel on import
try:
    from neomodel import config as neo_config
    neo_config.DATABASE_URL = f"{NEO4J_HOST}:{NEO4J_PORT}"
    # If host doesn't include bolt://, add it
    if not neo_config.DATABASE_URL.startswith("bolt://"):
        neo_config.DATABASE_URL = f"bolt://{NEO4J_USER}:{NEO4J_PASSWORD}@{NEO4J_HOST}:{NEO4J_PORT}"
    else:
        # Extract host from bolt:// URL and add credentials
        host_part = neo_config.DATABASE_URL.replace("bolt://", "")
        neo_config.DATABASE_URL = f"bolt://{NEO4J_USER}:{NEO4J_PASSWORD}@{host_part}:{NEO4J_PORT}"
except ImportError:
    # neomodel not installed, skip configuration
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
