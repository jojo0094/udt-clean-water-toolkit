# Transform Module - GIS to Graph Transformations

This module contains classes for transforming GIS (Geographic Information System) data into various graph representations.

## Understanding Data Structures

**Before working with this module**, familiarize yourself with the data structures by reading:
- **`../core/schemas.py`** - Complete documentation of all node and edge types
- **`../core/README.md`** - Quick reference guide

## Key Concepts

### What is a Node?
A **node** represents a point in the water network:
- **PipeNode**: A junction (where pipes connect) or end point (where a pipe terminates)
- **AssetNode**: A physical asset like a valve, hydrant, or meter

Each node has:
- `node_key`: Unique identifier
- `coords_27700`: Location in British National Grid coordinates
- `node_labels`: Type labels (e.g., ["NetworkNode", "PipeNode", "PipeJunction"])
- Additional attributes depending on type

### What is an Edge?
An **edge** represents a connection in the water network:
- **PipeEdge**: A physical pipe segment connecting two pipe nodes
- **PipeToAssetEdge**: A connection between a pipe node and an asset at the same location

Each edge has:
- `from_node_key`: Starting node
- `to_node_key`: Ending node
- `edge_key`: Unique identifier (format: "from_node_key-to_node_key")
- Additional attributes (for PipeEdge: material, diameter, length, etc.)

### List Structures

Throughout the code, you'll encounter these list structures:

```python
# List of lists - one inner list per pipe
all_pipe_edges_by_pipe: List[List[PipeEdge]]
# Example: [[edge1, edge2], [edge3, edge4, edge5]]
# Two pipes: first has 2 segments, second has 3 segments

all_pipe_nodes_by_pipe: List[List[PipeNode]]  
# Example: [[node1, node2, node3], [node4, node5]]
# Two pipes: first has 3 nodes, second has 2 nodes

# Triple-nested list - organized by [pipe][position][assets_at_position]
all_asset_nodes_by_pipe: List[List[List[AssetNode]]]
# Example: [[[valve1], []], [[hydrant1, meter1]]]
# First pipe: valve at first position, nothing at second
# Second pipe: hydrant and meter at first position

all_pipe_node_to_asset_node_edges: List[List[PipeToAssetEdge]]
# Example: [[edge1], [edge2, edge3]]
# Edges connecting pipe nodes to co-located assets
```

## Module Files

### `gis_to_graph.py`
Base class for converting GIS data to graph representations.
- Processes pipe geometries and point assets
- Creates nodes and edges
- Handles parallel processing for large datasets

### `gis_to_neo4j.py`
Extends `GisToGraph` to create Neo4j graph databases.
- Batch creates nodes and edges in Neo4j
- Handles DMA (District Metered Area) and utility relationships

### `gis_to_networkx.py`
Converts GIS data to NetworkX graph format.

### `gis_to_networkit.py`
Converts GIS data to NetworKit graph format for high-performance analysis.

### `neo4j_to_nk.py`
Converts Neo4j graphs to NetworKit format.

### `neo4j_to_wntr.py`
Converts Neo4j graphs to WNTR (Water Network Tool for Resilience) format.

## Example: Understanding a PipeEdge

When you see `all_pipe_edges_by_pipe`, each edge is a dictionary:

```python
{
    "from_node_key": "abc123",      # Where this segment starts
    "to_node_key": "def456",        # Where this segment ends
    "edge_key": "abc123-def456",    # Unique ID for this edge
    "tag": "PIPE_12345",            # Pipe identifier
    "material": "Cast Iron",        # What the pipe is made of
    "diameter": 150.0,              # Pipe diameter in mm
    "segment_length": 45.67823,     # Length of this segment in meters
    "segment_wkt": "LINESTRING (...)", # Geometry of this segment
    # ... plus DMA and utility information
}
```

See `../core/schemas.py` for complete documentation of all attributes.

## Quick Reference

| Term | Meaning |
|------|---------|
| `node_key` | Unique identifier for a node, encoded from its location and type |
| `edge_key` | Unique identifier for an edge: "{from_node_key}-{to_node_key}" |
| `PipeNode` | Junction or end point on a pipe |
| `AssetNode` | Physical asset (valve, hydrant, meter, etc.) |
| `PipeEdge` | Pipe segment connecting two pipe nodes |
| `PipeToAssetEdge` | Link between pipe node and co-located asset |
| `DMA` | District Metered Area - a zone in the water network |
| `coords_27700` | Coordinates in EPSG:27700 (British National Grid) |

## Getting Help

If you're confused about:
- **Data structures**: Read `../core/schemas.py`
- **Data flow**: Follow the examples in `../core/README.md`
- **Specific implementations**: Check the docstrings in each module file
