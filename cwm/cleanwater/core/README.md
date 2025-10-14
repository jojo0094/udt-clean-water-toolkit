# Core Module - Data Structures and Schemas

This directory contains core utilities and schema definitions for the Clean Water Toolkit.

## Schema Documentation

### `schemas.py` - Data Structure Definitions

The `schemas.py` module provides comprehensive documentation and type definitions for all data structures used throughout the toolkit. If you're having difficulty understanding data flow and object types, **start here**.

#### Key Data Structures

**Nodes (Network Vertices):**
- **`PipeNode`**: Represents junctions and end points on pipes where pipes connect or terminate
  - Contains: node_key, coordinates, labels, pipe_tags, DMA info, utility info
  - Example use: Where two pipes meet (junction) or where a pipe ends

- **`AssetNode`**: Represents physical infrastructure assets (valves, hydrants, meters, etc.)
  - Contains: node_key, coordinates, labels, tag, asset_name, subtype, acoustic_logger
  - Example use: A valve installed at a specific location in the network

**Edges (Network Connections):**
- **`PipeEdge`**: Represents a physical pipe segment connecting two pipe nodes
  - Contains: from/to node keys, edge_key, pipe properties (material, diameter, length)
  - Example use: The pipe segment running from junction A to junction B

- **`PipeToAssetEdge`**: Represents the connection between a pipe node and an asset at the same location
  - Contains: from/to node keys, edge_key
  - Example use: Links a junction to a valve installed at that junction

#### List Structures

Throughout the codebase, you'll see these collection types:

- `all_pipe_edges_by_pipe`: List of lists of PipeEdge objects, organized by pipe
- `all_pipe_nodes_by_pipe`: List of lists of PipeNode objects, organized by pipe
- `all_asset_nodes_by_pipe`: List of lists of lists - organized by pipe, then position, then assets at that position
- `all_pipe_node_to_asset_node_edges`: List of lists of PipeToAssetEdge objects

#### Example Usage

```python
from cleanwater.core.schemas import PipeNode, AssetNode, PipeEdge, PipeToAssetEdge

# Understanding what's in a pipe node
pipe_node: PipeNode = {
    "node_key": "abc123",
    "coords_27700": [532145.7, 181456.3],
    "utility": "Thames Water",
    "dma_codes": ["DMA001"],
    "dma_names": ["Central District"],
    "dmas": ["DMA001"],
    "node_labels": ["NetworkNode", "PipeNode", "PipeJunction"],
    "pipe_tags": ["PIPE_12345"]
}

# Understanding what's in an edge
pipe_edge: PipeEdge = {
    "from_node_key": "abc123",
    "to_node_key": "def456",
    "edge_key": "abc123-def456",
    "tag": "PIPE_12345",
    "pipe_type": "MainPipe",
    "material": "Cast Iron",
    "diameter": 150.0,
    # ... and more attributes documented in schemas.py
}
```

## Other Files

- `constants.py`: Constant values used throughout the application
- `utils.py`: Utility functions
- `db/`: Database-related utilities
