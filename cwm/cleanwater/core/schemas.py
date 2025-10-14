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

Attributes are documented in each TypedDict below.
"""

from typing import TypedDict, List, Optional


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
