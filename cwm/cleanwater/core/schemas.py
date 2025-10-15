"""
Schema definitions for data structures used in the Clean Water Toolkit.

This module defines the structure and types for nodes and edges in the water network graph.
These schemas help understand the data flow and object types throughout the codebase.

Node Types:
-----------
- PipeNode: Represents a junction or end point on a pipe (e.g., where pipes connect or terminate)
- AssetNode: Represents physical assets like valves, hydrants, meters, etc.
- NetworkNode: Base properties shared by all network nodes

Edge Types:
-----------
- PipeEdge: Represents a connection between two pipe nodes along a pipe segment
- PipeToAssetEdge: Represents a connection between a pipe node and an asset node

Data Structures:
---------------
- BasePipeData: Base pipeline segment data extracted from database queryset

Attributes are documented in each TypedDict below.
"""

from typing import TypedDict, List, Optional, Any, Tuple


# Type aliases for geometric data structures

Coords = List[List[float]]
"""
Type alias for coordinate data used in geometric operations.

Represents a list of coordinate pairs [x, y] for LineString or Polygon geometries.
Each inner list contains [x, y] coordinates as floats.

Examples:
    LineString coordinates: [[532145.7, 181456.3], [532150.2, 181460.8]]
    Point coordinates: [532145.7, 181456.3] (single coordinate pair)
"""

NormPointPosition = Tuple[float, float]
"""
Type alias for normalized point position data.

Returns a tuple containing:
    - distance_from_line_start (float): The actual distance from the start of the line to the point
    - normalised_position_on_line (float): The normalized position (0.0 to 1.0) along the line

Example:
    (45.67823, 0.234) means the point is 45.67823 units from the start and at 23.4% along the line
"""


class NetworkNodeBase(TypedDict):
    """
    Base schema for all network nodes.
    
    Attributes:
        node_key (str): Unique identifier for the node, encoded based on its geometry and type.
                       Format: encoded string generated using sqids from coordinates and type index.
        coords_27700 (List[float]): Coordinates of the node in EPSG:27700 projection [x, y].
        utility (str): Name of the utility company that owns/operates this node.
        dma_codes (List[str]): List of District Metered Area (DMA) codes associated with this node.
        dma_names (List[str]): List of human-readable DMA names associated with this node.
        dmas (List[str]): List of DMA identifiers.
    """
    node_key: str
    coords_27700: List[float]
    utility: str
    dma_codes: List[str]
    dma_names: List[str]
    dmas: List[str]


class PipeNode(NetworkNodeBase):
    """
    Schema for pipe network nodes (junctions and end points).
    
    A PipeNode represents a point on a pipe where:
    - Multiple pipes connect (junction)
    - A pipe terminates (end point)
    
    Attributes:
        node_labels (List[str]): Labels identifying the node type.
                                 Examples: ["NetworkNode", "PipeNode", "PipeJunction"]
                                          ["NetworkNode", "PipeNode", "PipeEnd"]
        pipe_tags (List[str]): Tags or identifiers associated with the pipe(s) at this node.
    
    Example:
        {
            "node_key": "abc123def456",
            "coords_27700": [532145.7, 181456.3],
            "utility": "Thames Water",
            "dma_codes": ["DMA001"],
            "dma_names": ["Central District"],
            "dmas": ["DMA001"],
            "node_labels": ["NetworkNode", "PipeNode", "PipeJunction"],
            "pipe_tags": ["PIPE_12345"]
        }
    """
    node_labels: List[str]
    pipe_tags: List[str]


class AssetNode(NetworkNodeBase):
    """
    Schema for asset nodes (physical infrastructure assets).
    
    An AssetNode represents a physical asset in the water network such as:
    - Valves (isolation valves, control valves, etc.)
    - Hydrants (fire hydrants)
    - Meters (flow meters, pressure meters)
    - Other point assets
    
    Attributes:
        node_labels (List[str]): Labels identifying the asset type.
                                 Examples: ["NetworkNode", "PointAsset", "Valve"]
                                          ["NetworkNode", "PointAsset", "Hydrant"]
        tag (str): Unique identifier or tag for the asset.
        asset_name (str): Type/category of the asset (e.g., "Valve", "Hydrant", "Meter").
        subtype (Optional[str]): More specific classification of the asset 
                                (e.g., "IsolationValve", "ControlValve").
        acoustic_logger (Optional[bool]): Whether this asset has an acoustic logger installed
                                         (used for leak detection).
    
    Example:
        {
            "node_key": "xyz789ghi012",
            "coords_27700": [532150.2, 181460.8],
            "utility": "Thames Water",
            "dma_codes": ["DMA001"],
            "dma_names": ["Central District"],
            "dmas": ["DMA001"],
            "node_labels": ["NetworkNode", "PointAsset", "Valve"],
            "tag": "VLV_54321",
            "asset_name": "Valve",
            "subtype": "IsolationValve",
            "acoustic_logger": False
        }
    """
    node_labels: List[str]
    tag: str
    asset_name: str
    subtype: Optional[str]
    acoustic_logger: Optional[bool]


class PipeEdge(TypedDict):
    """
    Schema for edges connecting pipe nodes along a pipe segment.
    
    A PipeEdge represents a physical pipe segment connecting two pipe nodes.
    This could be:
    - A segment between two junctions
    - A segment from a junction to an end point
    - A segment from a start point to a junction
    
    Attributes:
        from_node_key (str): node_key of the starting pipe node.
        to_node_key (str): node_key of the ending pipe node.
        edge_key (str): Unique identifier for this edge, formatted as "{from_node_key}-{to_node_key}".
        tag (str): Unique identifier or tag for the pipe.
        pipe_type (str): Type/classification of the pipe (e.g., "MainPipe", "ServicePipe").
        material (str): Material the pipe is made from (e.g., "Cast Iron", "PVC", "Steel").
        diameter (float): Internal diameter of the pipe in millimeters.
        asset_name (str): Name of the asset type (typically "Pipe" or specific pipe type).
        asset_label (str): Label used for categorizing the pipe asset.
        dma_codes (List[str]): DMA codes the pipe passes through.
        dma_names (List[str]): Human-readable DMA names the pipe passes through.
        dmas (List[str]): DMA identifiers the pipe is associated with.
        segment_length (float): Length of this pipe segment in meters, rounded to 5 decimal places.
        segment_wkt (str): Well-Known Text (WKT) representation of the pipe segment geometry.
                          Format: "LINESTRING (x1 y1, x2 y2, ...)"
    
    Example:
        {
            "from_node_key": "abc123def456",
            "to_node_key": "xyz789ghi012",
            "edge_key": "abc123def456-xyz789ghi012",
            "tag": "PIPE_12345",
            "pipe_type": "MainPipe",
            "material": "Cast Iron",
            "diameter": 150.0,
            "asset_name": "Pipe",
            "asset_label": "MainPipe",
            "dma_codes": ["DMA001"],
            "dma_names": ["Central District"],
            "dmas": ["DMA001"],
            "segment_length": 45.67823,
            "segment_wkt": "LINESTRING (532145.7 181456.3, 532150.2 181460.8)"
        }
    """
    from_node_key: str
    to_node_key: str
    edge_key: str
    tag: str
    pipe_type: str
    material: str
    diameter: float
    asset_name: str
    asset_label: str
    dma_codes: List[str]
    dma_names: List[str]
    dmas: List[str]
    segment_length: float
    segment_wkt: str


class PipeToAssetEdge(TypedDict):
    """
    Schema for edges connecting pipe nodes to asset nodes.
    
    A PipeToAssetEdge represents the spatial relationship between a pipe node
    (junction or end) and an asset (valve, hydrant, etc.) located at the same position.
    
    These edges are created when an asset is positioned at a pipe junction or end point,
    indicating that the asset is connected to that specific location in the pipe network.
    
    Attributes:
        from_node_key (str): node_key of the pipe node (PipeJunction or PipeEnd).
        to_node_key (str): node_key of the asset node (e.g., Valve, Hydrant).
        edge_key (str): Unique identifier for this edge, formatted as "{from_node_key}-{to_node_key}".
    
    Example:
        {
            "from_node_key": "abc123def456",
            "to_node_key": "mno345pqr678",
            "edge_key": "abc123def456-mno345pqr678"
        }
    
    Use Case:
        When a valve is installed at a pipe junction, a PipeToAssetEdge connects
        the junction node to the valve node, indicating their physical co-location
        and functional relationship.
    """
    from_node_key: str
    to_node_key: str
    edge_key: str


# Type aliases for collections of nodes and edges
# These represent the list structures used throughout the codebase

# List of pipe edges, one list per pipe in the network
AllPipeEdgesByPipe = List[List[PipeEdge]]

# List of pipe nodes, one list per pipe in the network
AllPipeNodesByPipe = List[List[PipeNode]]

# List of asset nodes, organized by pipe (list of lists)
# Inner list contains all assets at a particular position on a pipe
# Outer list contains all positions along each pipe
AllAssetNodesByPipe = List[List[List[AssetNode]]]

# List of edges connecting pipe nodes to asset nodes
AllPipeNodeToAssetNodeEdges = List[List[PipeToAssetEdge]]


# Additional schemas for supporting data structures

class DMAData(TypedDict):
    """
    Schema for District Metered Area (DMA) data.
    
    Attributes:
        node_key (str): The node key this DMA data is associated with.
        dma_codes (List[str]): DMA codes.
        dma_names (List[str]): Human-readable DMA names.
        dmas (List[str]): DMA identifiers.
    """
    node_key: str
    dma_codes: List[str]
    dma_names: List[str]
    dmas: List[str]


class UtilityData(TypedDict):
    """
    Schema for utility (water company) data.
    
    Attributes:
        node_key (str): The node key this utility data is associated with.
        utility (str): Name of the utility company.
    """
    node_key: str
    utility: str


class BasePipeData(TypedDict):
    """
    Schema for base pipeline segment data extracted from database queryset.
    
    This structure is returned by _get_base_pipe_data() and contains all the
    fundamental information about a pipe segment needed for graph construction.
    
    Attributes:
        id (int): The primary key of the pipeline segment.
        tag (str): The tag associated with the pipeline segment.
        pipe_type (str): The type of the pipe (e.g., "trunk_main", "distribution_main").
        asset_name (str): The name of the pipe asset (e.g., "pipe_main").
        asset_label (str): The label of the pipe asset (typically same as asset_name).
        pipe_length (float): The length of the pipe in meters.
        wkt (str): The Well-Known Text (WKT) representation of the pipe's geometry.
        material (str): The material of the pipe (e.g., "Cast Iron", "PVC").
        diameter (float): The diameter of the pipe in millimeters.
        dma_ids (List[int]): The IDs of the associated District Metered Areas (DMAs).
        dma_codes (List[str]): The codes of the associated DMAs.
        dma_names (List[str]): The names of the associated DMAs.
        dmas (str): A JSON string representation of the DMA data.
        utilities (List[str]): The names of utilities associated with the pipeline.
        geometry (Any): The geometric data of the pipeline segment (Django GEOSGeometry).
        start_point_geom (Any): The geometry of the pipeline's start point (Shapely Point).
        end_point_geom (Any): The geometry of the pipeline's end point (Shapely Point).
        line_start_intersection_tags (List[str]): Tags from the intersections at the start of the pipe.
        line_start_intersection_ids (List[int]): IDs from the intersections at the start of the pipe.
        line_end_intersection_tags (List[str]): Tags from the intersections at the end of the pipe.
        line_end_intersection_ids (List[int]): IDs from the intersections at the end of the pipe.
    
    Example:
        {
            "id": 12345,
            "tag": "PIPE_12345",
            "pipe_type": "trunk_main",
            "asset_name": "pipe_main",
            "asset_label": "pipe_main",
            "pipe_length": 123.456,
            "wkt": "LINESTRING (532145.7 181456.3, 532150.2 181460.8)",
            "material": "Cast Iron",
            "diameter": 150.0,
            "dma_ids": [1, 2],
            "dma_codes": ["DMA001", "DMA002"],
            "dma_names": ["Central District", "East District"],
            "dmas": '[{"code": "DMA001", "name": "Central District"}]',
            "utilities": ["Thames Water"],
            "geometry": <GEOSGeometry object>,
            "start_point_geom": <Point object>,
            "end_point_geom": <Point object>,
            "line_start_intersection_tags": [],
            "line_start_intersection_ids": [],
            "line_end_intersection_tags": [],
            "line_end_intersection_ids": []
        }
    """
    id: int
    tag: str
    pipe_type: str
    asset_name: str
    asset_label: str
    pipe_length: float
    wkt: str
    material: str
    diameter: float
    dma_ids: List[int]
    dma_codes: List[str]
    dma_names: List[str]
    dmas: str
    utilities: List[str]
    geometry: Any
    start_point_geom: Any
    end_point_geom: Any
    line_start_intersection_tags: List[str]
    line_start_intersection_ids: List[int]
    line_end_intersection_tags: List[str]
    line_end_intersection_ids: List[int]
