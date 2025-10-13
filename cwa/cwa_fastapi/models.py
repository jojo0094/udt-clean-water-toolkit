from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime
from database import Base
from constants import PIPE_MAIN__NAME, HYDRANT__NAME, NETWORK_OPT_VALVE__NAME

# Association tables for many-to-many relationships
pipe_main_dma = Table('assets_pipemain_dmas', Base.metadata,
    Column('pipemain_id', Integer, ForeignKey('assets_pipemain.id')),
    Column('dma_id', Integer, ForeignKey('utilities_dma.id'))
)

hydrant_dma = Table('assets_hydrant_dmas', Base.metadata,
    Column('hydrant_id', Integer, ForeignKey('assets_hydrant.id')),
    Column('dma_id', Integer, ForeignKey('utilities_dma.id'))
)

valve_dma = Table('assets_networkoptvalve_dmas', Base.metadata,
    Column('networkoptvalve_id', Integer, ForeignKey('assets_networkoptvalve.id')),
    Column('dma_id', Integer, ForeignKey('utilities_dma.id'))
)

class Utility(Base):
    __tablename__ = 'utilities_utility'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dmas = relationship("DMA", back_populates="utility")

class DMA(Base):
    __tablename__ = 'utilities_dma'
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    utility_id = Column(Integer, ForeignKey('utilities_utility.id'), nullable=False)
    network_repr = Column(JSON, nullable=True)
    geometry = Column(Geometry('MULTIPOLYGON', srid=27700), nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    utility = relationship("Utility", back_populates="dmas")
    pipe_mains = relationship("PipeMain", secondary=pipe_main_dma, back_populates="dmas")
    hydrants = relationship("Hydrant", secondary=hydrant_dma, back_populates="dmas")
    valves = relationship("NetworkOptValve", secondary=valve_dma, back_populates="dmas")

class PipeMain(Base):
    __tablename__ = 'assets_pipemain'
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, nullable=False, unique=True, index=True)
    geometry = Column(Geometry('LINESTRING', srid=27700), nullable=False)
    geometry_4326 = Column(Geometry('LINESTRING', srid=4326), nullable=False)
    material = Column(String(255), nullable=False, index=True)
    pipe_type = Column(String(255), nullable=False, index=True)
    diameter = Column(Float, nullable=False)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dmas = relationship("DMA", secondary=pipe_main_dma, back_populates="pipe_mains")
    flow = relationship("PipeFlow", back_populates="pipe_main", uselist=False)
    
    # Add pk property for compatibility with Django ORM
    @property
    def pk(self):
        return self.id
    
    # Add AssetMeta for compatibility with GisToGraph
    class AssetMeta:
        asset_name = PIPE_MAIN__NAME

class Hydrant(Base):
    __tablename__ = 'assets_hydrant'
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), nullable=False, unique=True, index=True)
    geometry = Column(Geometry('POINT', srid=27700), nullable=False)
    geometry_4326 = Column(Geometry('POINT', srid=4326), nullable=False)
    acoustic_logger = Column(Boolean, nullable=True)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dmas = relationship("DMA", secondary=hydrant_dma, back_populates="hydrants")
    
    # Add pk property for compatibility with Django ORM
    @property
    def pk(self):
        return self.id
    
    # Add AssetMeta for compatibility with GisToGraph
    class AssetMeta:
        asset_name = HYDRANT__NAME

class NetworkOptValve(Base):
    __tablename__ = 'assets_networkoptvalve'
    
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(50), nullable=False, unique=True, index=True)
    geometry = Column(Geometry('POINT', srid=27700), nullable=False)
    geometry_4326 = Column(Geometry('POINT', srid=4326), nullable=False)
    acoustic_logger = Column(Boolean, nullable=True)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dmas = relationship("DMA", secondary=valve_dma, back_populates="valves")
    
    # Add pk property for compatibility with Django ORM
    @property
    def pk(self):
        return self.id
    
    # Add AssetMeta for compatibility with GisToGraph
    class AssetMeta:
        asset_name = NETWORK_OPT_VALVE__NAME

class PipeFlow(Base):
    __tablename__ = 'waterpipes_pipeflow'
    
    pipe_main_id = Column(Integer, ForeignKey('assets_pipemain.id'), primary_key=True)
    flow_data = Column(JSON, nullable=False)
    
    pipe_main = relationship("PipeMain", back_populates="flow")
