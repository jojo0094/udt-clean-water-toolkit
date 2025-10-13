import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection configuration
POSTGIS_DB_NAME = os.getenv("POSTGIS_DB_NAME__ENV_VAR", "postgis")
POSTGIS_DB_USER = os.getenv("POSTGIS_DB_USER__ENV_VAR", "postgis")
POSTGIS_DB_PASSWORD = os.getenv("POSTGIS_DEFAULT_DB_PASSWORD__ENV_VAR", "postgis")
POSTGIS_DB_HOST = os.getenv("POSTGIS_DEFAULT_DB_HOST__ENV_VAR", "udtpostgis")
POSTGIS_DB_PORT = os.getenv("POSTGIS_DEFAULT_PORT__ENV_VAR", "5432")

DATABASE_URL = f"postgresql://{POSTGIS_DB_USER}:{POSTGIS_DB_PASSWORD}@{POSTGIS_DB_HOST}:{POSTGIS_DB_PORT}/{POSTGIS_DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
