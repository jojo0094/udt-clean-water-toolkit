# Type Annotations Guide for GIS to Graph Module

## Overview

This guide explains the type annotations added to the `gis_to_graph.py` module and how to use them effectively.

## New TypedDict Schemas

### BasePipeData

The `BasePipeData` TypedDict defines the structure of pipeline segment data returned by `_get_base_pipe_data()`. This schema provides type safety and autocomplete support when working with pipe data.

```python
from cleanwater.core.schemas import BasePipeData

# Example usage:
def process_pipe(base_pipe: BasePipeData) -> None:
    # Now your IDE knows what keys are available
    pipe_id = base_pipe["id"]  # int
    pipe_tag = base_pipe["tag"]  # str
    pipe_material = base_pipe["material"]  # str
    pipe_diameter = base_pipe["diameter"]  # float
    dma_codes = base_pipe["dma_codes"]  # List[str]
    # ... and many more!
```

#### Available Keys in BasePipeData:

- `id` (int): Primary key of the pipeline segment
- `tag` (str): Tag/identifier for the pipe
- `pipe_type` (str): Type of pipe (e.g., "trunk_main", "distribution_main")
- `asset_name` (str): Name of the pipe asset
- `asset_label` (str): Label for the pipe asset
- `pipe_length` (float): Length of the pipe in meters
- `wkt` (str): Well-Known Text geometry representation
- `material` (str): Pipe material (e.g., "Cast Iron", "PVC")
- `diameter` (float): Pipe diameter in millimeters
- `dma_ids` (List[int]): IDs of associated District Metered Areas
- `dma_codes` (List[str]): DMA codes
- `dma_names` (List[str]): DMA names
- `dmas` (str): JSON string of DMA data
- `utilities` (List[str]): Associated utility company names
- `geometry` (Any): GEOSGeometry object
- `start_point_geom` (Any): Shapely Point for pipe start
- `end_point_geom` (Any): Shapely Point for pipe end
- `line_start_intersection_tags` (List[str]): Tags of intersecting pipes at start
- `line_start_intersection_ids` (List[int]): IDs of intersecting pipes at start
- `line_end_intersection_tags` (List[str]): Tags of intersecting pipes at end
- `line_end_intersection_ids` (List[int]): IDs of intersecting pipes at end

## Method Type Annotations

All methods in `GisToGraph` class now have complete type annotations. Here are some examples:

### Public Methods

```python
# Reset internal data structures
def reset_pipe_asset_data(self) -> None:
    ...

# Get the SRID
def get_srid(self) -> int:
    ...

# Create DMA data for a node
def create_dma_data(self, node_data: dict) -> List[dict]:
    ...

# Build DMA data as JSON
@staticmethod
def build_dma_data_as_json(dma_codes: List[str], dma_names: List[str]) -> str:
    ...
```

### Private Methods

```python
# Get base pipe data from queryset
def _get_base_pipe_data(self, qs_object: Any) -> BasePipeData:
    ...

# Get edges for a pipe
def _get_edges_by_pipe(
    self, 
    base_pipe: BasePipeData, 
    nodes_by_pipe: List[PipeNode]
) -> List[PipeEdge]:
    ...

# Set nodes and edges
def _set_nodes_and_edges(
    self, 
    base_pipe: BasePipeData, 
    nodes_ordered: List[dict]
) -> Tuple[
    List[PipeNode], 
    List[PipeEdge], 
    List[List[AssetNode]], 
    List[PipeToAssetEdge], 
    List[dict], 
    List[dict], 
    List[str]
]:
    ...
```

## Benefits

### 1. Code Completion
IDEs like VSCode, PyCharm, and others will now provide autocomplete suggestions when working with these data structures.

### 2. Type Safety
Static type checkers like `mypy` can validate that you're using the correct types:

```python
# This will be flagged by mypy if diameter is not a float
base_pipe["diameter"] = "150"  # Error: Expected float
```

### 3. Documentation
The type annotations serve as inline documentation, making it clear what each method expects and returns.

### 4. Better Refactoring
When refactoring, type annotations help ensure you don't accidentally break existing code by changing types.

## Using Type Checking

To enable type checking in your development workflow:

```bash
# Install mypy
pip install mypy

# Run type checking
mypy cwm/cleanwater/transform/gis_to_graph.py

# Or check specific function
mypy -c "from cleanwater.transform.gis_to_graph import GisToGraph"
```

## IDE Configuration

### VSCode

Add to `.vscode/settings.json`:
```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.linting.mypyEnabled": true
}
```

### PyCharm

1. Go to Settings → Editor → Inspections
2. Enable "Python → Type checker"
3. Select "Mypy" as the type checker

## Related Schemas

The following schemas are also available in `cleanwater.core.schemas`:

- `PipeNode`: Junction or end points on pipes
- `AssetNode`: Physical assets (valves, hydrants, etc.)
- `PipeEdge`: Pipe segments connecting nodes
- `PipeToAssetEdge`: Connections between pipe nodes and assets
- `DMAData`: District Metered Area data
- `UtilityData`: Utility company data

## Example: Working with Type Annotations

```python
from typing import List
from cleanwater.core.schemas import BasePipeData, PipeNode, PipeEdge
from cleanwater.transform.gis_to_graph import GisToGraph

def process_pipes(gis_to_graph: GisToGraph, pipes: List[Any]) -> None:
    """Process a list of pipe queryset objects."""
    for pipe_qs in pipes:
        # Get base pipe data - now we know the structure!
        base_pipe: BasePipeData = gis_to_graph._get_base_pipe_data(pipe_qs)
        
        # Access properties with confidence
        print(f"Processing pipe {base_pipe['tag']}")
        print(f"Material: {base_pipe['material']}")
        print(f"Diameter: {base_pipe['diameter']}mm")
        print(f"Length: {base_pipe['pipe_length']}m")
        
        # Work with DMA codes
        for dma_code in base_pipe['dma_codes']:
            print(f"  DMA: {dma_code}")
```

## Testing

Tests have been added in `cwm/tests/test_schemas.py` to verify the schema definitions. Run them with:

```bash
pytest cwm/tests/test_schemas.py -v
```

## Future Enhancements

Consider these potential improvements:

1. Create more specific TypedDicts for intermediate data structures
2. Add runtime validation using libraries like `pydantic`
3. Generate OpenAPI/JSON Schema documentation from TypedDicts
4. Add type stubs for external dependencies

## Questions?

For questions or issues related to type annotations:

1. Check the schema definitions in `cwm/cleanwater/core/schemas.py`
2. Review the docstrings in `cwm/cleanwater/transform/gis_to_graph.py`
3. Look at tests in `cwm/tests/test_schemas.py` for usage examples
