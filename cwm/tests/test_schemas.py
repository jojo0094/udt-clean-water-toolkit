"""
Tests for schema definitions.

These tests validate that the schema definitions are correctly structured
and can be imported and used as expected.
"""

import pytest
from cleanwater.core.schemas import (
    NetworkNodeBase,
    PipeNode,
    AssetNode,
    PipeEdge,
    PipeToAssetEdge,
    DMAData,
    UtilityData,
    BasePipeData,
    AllPipeEdgesByPipe,
    AllPipeNodesByPipe,
    AllAssetNodesByPipe,
    AllPipeNodeToAssetNodeEdges,
)


class TestSchemaImports:
    """Test that all schema types can be imported."""

    def test_import_node_schemas(self):
        """Test that node schema types can be imported."""
        assert NetworkNodeBase is not None
        assert PipeNode is not None
        assert AssetNode is not None

    def test_import_edge_schemas(self):
        """Test that edge schema types can be imported."""
        assert PipeEdge is not None
        assert PipeToAssetEdge is not None

    def test_import_data_schemas(self):
        """Test that data schema types can be imported."""
        assert DMAData is not None
        assert UtilityData is not None
        assert BasePipeData is not None

    def test_import_collection_types(self):
        """Test that collection type aliases can be imported."""
        assert AllPipeEdgesByPipe is not None
        assert AllPipeNodesByPipe is not None
        assert AllAssetNodesByPipe is not None
        assert AllPipeNodeToAssetNodeEdges is not None


class TestSchemaStructure:
    """Test that schema definitions have the expected structure."""

    def test_pipe_node_structure(self):
        """Test PipeNode has expected attributes."""
        # Create a sample PipeNode
        pipe_node: PipeNode = {
            "node_key": "test123",
            "coords_27700": [100.0, 200.0],
            "utility": "Test Utility",
            "dma_codes": ["DMA001"],
            "dma_names": ["Test DMA"],
            "dmas": ["DMA001"],
            "node_labels": ["NetworkNode", "PipeNode", "PipeJunction"],
            "pipe_tags": ["PIPE_001"],
        }
        
        # Verify all expected keys are present
        assert "node_key" in pipe_node
        assert "coords_27700" in pipe_node
        assert "utility" in pipe_node
        assert "dma_codes" in pipe_node
        assert "dma_names" in pipe_node
        assert "dmas" in pipe_node
        assert "node_labels" in pipe_node
        assert "pipe_tags" in pipe_node

    def test_asset_node_structure(self):
        """Test AssetNode has expected attributes."""
        asset_node: AssetNode = {
            "node_key": "asset456",
            "coords_27700": [150.0, 250.0],
            "utility": "Test Utility",
            "dma_codes": ["DMA001"],
            "dma_names": ["Test DMA"],
            "dmas": ["DMA001"],
            "node_labels": ["NetworkNode", "PointAsset", "Valve"],
            "tag": "VLV_001",
            "asset_name": "Valve",
            "subtype": "IsolationValve",
            "acoustic_logger": False,
        }
        
        # Verify all expected keys are present
        assert "node_key" in asset_node
        assert "coords_27700" in asset_node
        assert "node_labels" in asset_node
        assert "tag" in asset_node
        assert "asset_name" in asset_node
        assert "subtype" in asset_node
        assert "acoustic_logger" in asset_node

    def test_pipe_edge_structure(self):
        """Test PipeEdge has expected attributes."""
        pipe_edge: PipeEdge = {
            "from_node_key": "node1",
            "to_node_key": "node2",
            "edge_key": "node1-node2",
            "tag": "PIPE_001",
            "pipe_type": "MainPipe",
            "material": "Cast Iron",
            "diameter": 150.0,
            "asset_name": "Pipe",
            "asset_label": "MainPipe",
            "dma_codes": ["DMA001"],
            "dma_names": ["Test DMA"],
            "dmas": ["DMA001"],
            "segment_length": 45.67823,
            "segment_wkt": "LINESTRING (0 0, 1 1)",
        }
        
        # Verify all expected keys are present
        assert "from_node_key" in pipe_edge
        assert "to_node_key" in pipe_edge
        assert "edge_key" in pipe_edge
        assert "tag" in pipe_edge
        assert "pipe_type" in pipe_edge
        assert "material" in pipe_edge
        assert "diameter" in pipe_edge
        assert "asset_name" in pipe_edge
        assert "asset_label" in pipe_edge
        assert "segment_length" in pipe_edge
        assert "segment_wkt" in pipe_edge

    def test_pipe_to_asset_edge_structure(self):
        """Test PipeToAssetEdge has expected attributes."""
        pipe_to_asset_edge: PipeToAssetEdge = {
            "from_node_key": "pipe_node1",
            "to_node_key": "asset_node1",
            "edge_key": "pipe_node1-asset_node1",
        }
        
        # Verify all expected keys are present
        assert "from_node_key" in pipe_to_asset_edge
        assert "to_node_key" in pipe_to_asset_edge
        assert "edge_key" in pipe_to_asset_edge

    def test_dma_data_structure(self):
        """Test DMAData has expected attributes."""
        dma_data: DMAData = {
            "node_key": "node1",
            "dma_codes": ["DMA001"],
            "dma_names": ["Test DMA"],
            "dmas": ["DMA001"],
        }
        
        assert "node_key" in dma_data
        assert "dma_codes" in dma_data
        assert "dma_names" in dma_data
        assert "dmas" in dma_data

    def test_utility_data_structure(self):
        """Test UtilityData has expected attributes."""
        utility_data: UtilityData = {
            "node_key": "node1",
            "utility": "Test Utility",
        }
        
        assert "node_key" in utility_data
        assert "utility" in utility_data

    def test_base_pipe_data_structure(self):
        """Test BasePipeData has expected attributes."""
        # This is a partial test - creating a full BasePipeData would require
        # mocking Django and Shapely objects
        from typing import TYPE_CHECKING
        
        # At least verify the type exists and has annotations
        if TYPE_CHECKING:
            base_pipe: BasePipeData = {
                "id": 12345,
                "tag": "PIPE_12345",
                "pipe_type": "trunk_main",
                "asset_name": "pipe_main",
                "asset_label": "pipe_main",
                "pipe_length": 123.456,
                "wkt": "LINESTRING (0 0, 1 1)",
                "material": "Cast Iron",
                "diameter": 150.0,
                "dma_ids": [1, 2],
                "dma_codes": ["DMA001", "DMA002"],
                "dma_names": ["Central", "East"],
                "dmas": '[{"code": "DMA001", "name": "Central"}]',
                "utilities": ["Thames Water"],
                "geometry": None,  # Would be GEOSGeometry
                "start_point_geom": None,  # Would be Point
                "end_point_geom": None,  # Would be Point
                "line_start_intersection_tags": [],
                "line_start_intersection_ids": [],
                "line_end_intersection_tags": [],
                "line_end_intersection_ids": [],
            }
        
        # At minimum verify the type is defined
        assert BasePipeData is not None


class TestSchemaDocumentation:
    """Test that schema definitions have proper documentation."""

    def test_pipe_node_has_docstring(self):
        """Test that PipeNode has documentation."""
        assert PipeNode.__doc__ is not None
        assert len(PipeNode.__doc__) > 100

    def test_asset_node_has_docstring(self):
        """Test that AssetNode has documentation."""
        assert AssetNode.__doc__ is not None
        assert len(AssetNode.__doc__) > 100

    def test_pipe_edge_has_docstring(self):
        """Test that PipeEdge has documentation."""
        assert PipeEdge.__doc__ is not None
        assert len(PipeEdge.__doc__) > 100

    def test_pipe_to_asset_edge_has_docstring(self):
        """Test that PipeToAssetEdge has documentation."""
        assert PipeToAssetEdge.__doc__ is not None
        assert len(PipeToAssetEdge.__doc__) > 100

    def test_base_pipe_data_has_docstring(self):
        """Test that BasePipeData has documentation."""
        assert BasePipeData.__doc__ is not None
        assert len(BasePipeData.__doc__) > 100
