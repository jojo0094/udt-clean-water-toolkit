# Schema Documentation Implementation Summary

This document summarizes the schema documentation added to address the issue about understanding data flow and object types in the `cwm` folder.

## Problem Statement

The original issue stated:
> "I am having difficulty understanding data flow and data object type. For example:
> - all_pipe_edges_by_pipe (list): List of edges for each pipe.
> - all_pipe_nodes_by_pipe (list): List of nodes for each pipe.
> 
> Is list of edges? But what is edge? What attributes it has? etc."

## Solution Implemented

### 1. Core Schema Definitions
**File**: `cwm/cleanwater/core/schemas.py`

Created comprehensive TypedDict definitions for all data structures:

#### Node Types:
- **`PipeNode`**: Junction or end points on pipes
  - Example attributes: `node_key`, `coords_27700`, `node_labels`, `pipe_tags`
  - Detailed docstring with real-world examples

- **`AssetNode`**: Physical assets (valves, hydrants, meters)
  - Example attributes: `node_key`, `tag`, `asset_name`, `subtype`, `acoustic_logger`
  - Detailed docstring explaining each attribute

#### Edge Types:
- **`PipeEdge`**: Pipe segments connecting two pipe nodes
  - Attributes: `from_node_key`, `to_node_key`, `edge_key`, `material`, `diameter`, `segment_length`, `segment_wkt`, etc.
  - Complete documentation of all properties

- **`PipeToAssetEdge`**: Connections between pipe nodes and assets
  - Attributes: `from_node_key`, `to_node_key`, `edge_key`
  - Explains the relationship between pipe nodes and co-located assets

#### Collection Types:
- **`AllPipeEdgesByPipe`**: Type alias for `List[List[PipeEdge]]`
- **`AllPipeNodesByPipe`**: Type alias for `List[List[PipeNode]]`
- **`AllAssetNodesByPipe`**: Type alias for `List[List[List[AssetNode]]]`
- **`AllPipeNodeToAssetNodeEdges`**: Type alias for `List[List[PipeToAssetEdge]]`

### 2. Data Flow Documentation
**File**: `cwm/cleanwater/DATA_FLOW.md`

Created a comprehensive guide with:
- ASCII diagrams showing how GIS data flows through the system
- Visual examples of a water network with 2 pipes
- Concrete examples showing exactly what data is in each list structure
- Common iteration patterns
- Explanations of key concepts (node_key, edge_key, coords_27700)

Example from the doc:
```python
# Example showing what's in all_pipe_edges_by_pipe
[
    # Pipe 1 edges
    [
        {"from_node_key": "A", "to_node_key": "B", 
         "material": "Cast Iron", "diameter": 150.0, ...},
        {"from_node_key": "B", "to_node_key": "C", ...}
    ],
    # Pipe 2 edges
    [
        {"from_node_key": "D", "to_node_key": "E", ...}
    ]
]
```

### 3. Quick Reference Guides
**Files**: 
- `cwm/cleanwater/core/README.md`
- `cwm/cleanwater/transform/README.md`

Created README files that:
- Explain what nodes and edges are
- Show how to use the schema definitions
- Provide quick reference tables
- Link to detailed documentation

### 4. Updated Existing Code
**Files Modified**:
- `cwm/cleanwater/transform/gis_to_graph.py`
- `cwm/cleanwater/transform/gis_to_neo4j.py`
- `cwm/cleanwater/core/__init__.py`

Added:
- Module-level docstrings pointing to schema documentation
- Enhanced class docstrings with specific type references
- Import statements to make schemas easily accessible

### 5. Tests
**File**: `cwm/tests/test_schemas.py`

Created 14 tests that:
- Validate all schema types can be imported
- Verify schema structure matches expected attributes
- Ensure documentation exists for all schemas
- Provide examples of how to use the schemas

All tests pass ✅

### 6. Main README Update
**File**: `cwm/README.md`

Added prominent section at the top directing users to:
- DATA_FLOW.md for understanding data structures
- schemas.py for complete type definitions
- README files for quick references

## How to Use This Documentation

### For New Developers
1. Start with `cwm/cleanwater/DATA_FLOW.md`
2. Look at examples in `cwm/cleanwater/core/schemas.py`
3. Refer to `cwm/cleanwater/core/README.md` for quick lookups

### For Existing Developers
1. Use `cwm/cleanwater/core/schemas.py` as a reference
2. Check `cwm/cleanwater/transform/README.md` for module-specific guidance
3. Import types: `from cleanwater.core.schemas import PipeNode, PipeEdge`

### Answer to Original Question

**Q: "Is list of edges? But what is edge? What attributes it has?"**

**A:** Yes, `all_pipe_edges_by_pipe` is a list of lists of edges. Each edge is a **dictionary** with these attributes:

```python
{
    "from_node_key": str,      # Starting node
    "to_node_key": str,        # Ending node
    "edge_key": str,           # Unique ID: "from-to"
    "tag": str,                # Pipe identifier
    "pipe_type": str,          # Type of pipe
    "material": str,           # What it's made of
    "diameter": float,         # Size in mm
    "asset_name": str,         # Asset type name
    "asset_label": str,        # Asset label
    "dma_codes": List[str],    # DMA codes
    "dma_names": List[str],    # DMA names
    "dmas": List[str],         # DMA identifiers
    "segment_length": float,   # Length in meters
    "segment_wkt": str         # Geometry as WKT
}
```

See `PipeEdge` in `cwm/cleanwater/core/schemas.py` for complete documentation.

## Files Created/Modified

### New Files Created:
1. `cwm/cleanwater/core/schemas.py` (270 lines)
2. `cwm/cleanwater/core/README.md` (95 lines)
3. `cwm/cleanwater/transform/README.md` (150 lines)
4. `cwm/cleanwater/DATA_FLOW.md` (260 lines)
5. `cwm/tests/test_schemas.py` (178 lines)

### Files Modified:
1. `cwm/README.md` - Added prominent documentation section
2. `cwm/cleanwater/core/__init__.py` - Added schema imports
3. `cwm/cleanwater/transform/gis_to_graph.py` - Enhanced docstrings
4. `cwm/cleanwater/transform/gis_to_neo4j.py` - Enhanced docstrings

### Total Impact:
- **953 lines** of new documentation
- **14 tests** (all passing)
- **0 breaking changes** to existing code
- **100% backward compatible**

## Benefits

1. ✅ **Clear Documentation**: Every data structure is now clearly documented
2. ✅ **Type Safety**: TypedDict definitions enable IDE autocomplete and type checking
3. ✅ **Examples**: Real-world examples show exactly what data looks like
4. ✅ **Testable**: Tests validate schema structure remains consistent
5. ✅ **Discoverable**: Multiple entry points (README, DATA_FLOW.md, schemas.py)
6. ✅ **Maintainable**: Changes to data structures should update schemas accordingly

## Next Steps

For future improvements, consider:
1. Using Pydantic models instead of TypedDict for runtime validation
2. Adding more visual diagrams or flowcharts
3. Creating example scripts that demonstrate using the data structures
4. Adding type hints throughout the codebase using these schema definitions
