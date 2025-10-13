"""
Adapter for GisToNeo4j to work with SQLAlchemy models instead of Django ORM.
This module provides a compatibility layer between FastAPI/SQLAlchemy and the 
cleanwater GisToNeo4j transformer.
"""

import sys
sys.path.append('/opt/udt/')

from cwm.cleanwater.transform.gis_to_neo4j import GisToNeo4j
from geoalchemy2.shape import to_shape
from shapely import Point
from shapely.wkt import loads as wkt_loads


class GisToNeo4jAdapter(GisToNeo4j):
    """
    Adapter class that extends GisToNeo4j to work with SQLAlchemy models.
    
    This class overrides methods that have Django-specific dependencies
    to make them work with SQLAlchemy/GeoAlchemy2 instead.
    """
    
    def __init__(self, srid, sqids, point_asset_names=None, db_session=None, **kwargs):
        """
        Initialize the adapter with SQLAlchemy database session.
        
        Args:
            srid: Spatial Reference System Identifier
            sqids: Sqids instance for ID generation
            point_asset_names: List of point asset names to include
            db_session: SQLAlchemy database session
            **kwargs: Additional arguments for parent class
        """
        super().__init__(
            srid=srid,
            sqids=sqids,
            point_asset_names=point_asset_names or [],
            **kwargs
        )
        self.db_session = db_session
    
    def _get_base_pipe_data(self, qs_object) -> dict:
        """
        Extract and organize the base data for a pipeline segment from a SQLAlchemy object.
        
        Overrides the parent method to work with SQLAlchemy models instead of Django ORM.
        
        Args:
            qs_object: SQLAlchemy PipeMain model instance
            
        Returns:
            dict: Dictionary containing the extracted data for the pipeline segment
        """
        base_pipe = {}
        
        # Convert GeoAlchemy2 geometry to shapely geometry
        geom_shapely = to_shape(qs_object.geometry)
        
        base_pipe["id"] = qs_object.pk
        base_pipe["tag"] = qs_object.tag
        base_pipe["pipe_type"] = qs_object.pipe_type
        base_pipe["asset_name"] = qs_object.AssetMeta.asset_name
        base_pipe["asset_label"] = qs_object.AssetMeta.asset_name
        base_pipe["pipe_length"] = geom_shapely.length
        base_pipe["wkt"] = geom_shapely.wkt
        base_pipe["material"] = qs_object.material
        base_pipe["diameter"] = qs_object.diameter
        
        # Handle DMAs - SQLAlchemy relationship
        dmas = qs_object.dmas
        base_pipe["dma_ids"] = [dma.id for dma in dmas]
        base_pipe["dma_codes"] = [dma.code for dma in dmas]
        base_pipe["dma_names"] = [dma.name for dma in dmas]
        base_pipe["dmas"] = self.build_dma_data_as_json(
            base_pipe["dma_codes"], base_pipe["dma_names"]
        )
        
        base_pipe["utilities"] = [dma.utility.name for dma in dmas]
        
        # For GisToGraph compatibility, we need to add a mock geometry object
        # that has the properties the code expects
        class GeometryWrapper:
            def __init__(self, shapely_geom):
                self._shapely = shapely_geom
                self.wkt = shapely_geom.wkt
                self.length = shapely_geom.length
                self.coords = list(shapely_geom.coords)
        
        base_pipe["geometry"] = GeometryWrapper(geom_shapely)
        base_pipe["start_point_geom"] = Point(geom_shapely.coords[0])
        base_pipe["end_point_geom"] = Point(geom_shapely.coords[-1])
        
        base_pipe["line_start_intersection_tags"] = []
        base_pipe["line_start_intersection_ids"] = []
        base_pipe["line_end_intersection_tags"] = []
        base_pipe["line_end_intersection_ids"] = []
        
        return base_pipe
    
    def _combine_all_pipe_junctions(self, pipe_qs_object) -> list:
        """
        Override to return empty list as junctions are handled by intersections.
        
        Args:
            pipe_qs_object: SQLAlchemy PipeMain model instance
            
        Returns:
            list: Empty list
        """
        return []
    
    def _combine_all_point_assets(self, pipe_qs_object) -> list:
        """
        Get all point assets that intersect with the given pipe using SQLAlchemy.
        
        Overrides the parent method to work with SQLAlchemy models instead of Django ORM.
        
        Args:
            pipe_qs_object: SQLAlchemy PipeMain model instance
            
        Returns:
            list: List of point asset dictionaries with their properties
        """
        if not self.db_session:
            return []
        
        from models import Hydrant, NetworkOptValve
        from geoalchemy2.functions import ST_Intersects
        
        assets_list = []
        
        # Map asset names to SQLAlchemy models
        asset_models = {
            "hydrant": Hydrant,
            "network_opt_valve": NetworkOptValve,
        }
        
        # Convert pipe geometry for intersection query
        pipe_geom = pipe_qs_object.geometry
        
        for asset_name in self.point_asset_names:
            if asset_name in asset_models:
                model = asset_models[asset_name]
                
                # Query for intersecting assets using PostGIS ST_Intersects
                intersecting_assets = self.db_session.query(model).filter(
                    ST_Intersects(model.geometry, pipe_geom)
                ).all()
                
                # Convert SQLAlchemy objects to dict format expected by GisToGraph
                for asset in intersecting_assets:
                    asset_geom = to_shape(asset.geometry)
                    asset_dict = {
                        "id": asset.pk,
                        "tag": asset.tag,
                        "wkt": asset_geom.wkt,
                        "asset_name": asset.AssetMeta.asset_name,
                        "asset_label": asset.AssetMeta.asset_name,
                        "geometry": asset_geom,
                    }
                    
                    # Add DMA information if available
                    if hasattr(asset, 'dmas') and asset.dmas:
                        asset_dict["dma_ids"] = [dma.id for dma in asset.dmas]
                        asset_dict["dma_codes"] = [dma.code for dma in asset.dmas]
                        asset_dict["dma_names"] = [dma.name for dma in asset.dmas]
                        asset_dict["utilities"] = [dma.utility.name for dma in asset.dmas]
                    else:
                        asset_dict["dma_ids"] = []
                        asset_dict["dma_codes"] = []
                        asset_dict["dma_names"] = []
                        asset_dict["utilities"] = []
                    
                    assets_list.append(asset_dict)
        
        return assets_list
