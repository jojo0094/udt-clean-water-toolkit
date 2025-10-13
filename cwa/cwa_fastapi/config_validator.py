"""
Configuration validation using Pydantic (non-Django).
This module provides configuration validation without Django dependencies.
"""

import configparser
from types import SimpleNamespace
from itertools import chain
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, model_validator


class ConfigModel(BaseModel):
    """
    Pydantic model for validating configuration parameters.
    Replaces Django forms-based validation.
    """
    
    method: str = Field(..., max_length=23, description="Processing method to use")
    neoj4_point: Optional[bool] = Field(False, description="Whether to use Neo4j point geometry")
    srid: int = Field(..., description="Spatial Reference System Identifier")
    batch_size: int = Field(..., description="Batch size for processing")
    chunk_size: Optional[int] = Field(None, description="Chunk size for parallel processing")
    query_limit: Optional[int] = Field(None, description="Query result limit")
    query_offset: Optional[int] = Field(None, description="Query result offset")
    parallel: Optional[bool] = Field(False, description="Whether to use parallel processing")
    thread_count: Optional[int] = Field(None, description="Number of threads for parallel processing")
    processor_count: Optional[int] = Field(None, description="Number of processors for parallel processing")
    inpfile: Optional[str] = Field(None, max_length=256, description="Input INP file path")
    outputfile: Optional[str] = Field(None, max_length=256, description="Output file path")
    dma_codes: Optional[str] = Field(None, max_length=256, description="Comma-separated DMA codes")
    utility_names: Optional[str] = Field(None, max_length=256, description="Comma-separated utility names")
    wntr_simulation_timestep_hours: Optional[float] = Field(None, description="WNTR simulation timestep in hours")
    wntr_simulation_length_hours: Optional[float] = Field(None, description="WNTR simulation length in hours")
    
    @field_validator('dma_codes')
    @classmethod
    def parse_dma_codes(cls, v):
        """Parse comma-separated DMA codes into a list."""
        if not v:
            return None
        try:
            codes = v.split(",")
            return [code.strip() for code in codes]
        except Exception:
            raise ValueError("Incorrect format for dma_codes")
    
    @field_validator('utility_names')
    @classmethod
    def parse_utility_names(cls, v):
        """Parse comma-separated utility names into a list."""
        if not v:
            return None
        try:
            names = v.split(",")
            return [name.strip() for name in names]
        except Exception:
            raise ValueError("Incorrect format for utility_names")
    
    @model_validator(mode='after')
    def validate_parallel_settings(self):
        """Validate parallel processing settings."""
        if self.parallel and not (self.thread_count or self.processor_count):
            raise ValueError(
                "If parallel is set to 'True' both 'thread_count' and 'processor_count' must be specified."
            )
        return self
    
    @model_validator(mode='after')
    def validate_outputfile(self):
        """Validate outputfile based on method."""
        if self.method in ("neo4j2wntrjson", "neo4j2wntrinp") and not self.outputfile:
            raise ValueError(
                "If 'method' is 'neo4j2wntrjson' or 'neo4j2wntrinp', 'outputfile' must be specified."
            )
        return self
    
    @model_validator(mode='after')
    def validate_inpfile(self):
        """Validate inpfile based on method."""
        if self.method == "inp2hydaulic" and not self.inpfile:
            raise ValueError(
                "If 'method' is 'inp2hydaulic', 'inpfile' must be specified."
            )
        return self
    
    @model_validator(mode='after')
    def validate_time_parameters(self):
        """Validate WNTR time parameters based on method."""
        if self.method in ("inp2hydaulic", "neo4j2wntrinp", "neo4j2wntrjson"):
            if not self.wntr_simulation_timestep_hours or not self.wntr_simulation_length_hours:
                raise ValueError(
                    "If 'method' is 'inp2hydaulic', 'neo4j2wntrinp', or 'neo4j2wntrjson', "
                    "'wntr_simulation_timestep_hours' and 'wntr_simulation_length_hours' must be specified."
                )
        return self


class AppConf:
    """
    Configuration parser that validates config files using Pydantic instead of Django.
    This is a drop-in replacement for the Django-based AppConf class.
    """
    
    def __init__(self, conf_file: str):
        """
        Set the config params from the conf file.
        
        Args:
            conf_file: Path to the configuration file
        """
        parser = configparser.ConfigParser()
        
        with open(conf_file) as lines:
            lines = chain(("[app_config]",), lines)  # Add section header
            parser.read_file(lines)
        
        self._validate_config(parser["app_config"])
    
    def _validate_config(self, parser_config):
        """
        Validate configuration using Pydantic model.
        
        Args:
            parser_config: ConfigParser section with configuration values
            
        Raises:
            ValueError: If validation fails
        """
        # Convert ConfigParser section to dict
        config_dict = dict(parser_config)
        
        # Convert string boolean values to actual booleans
        for key in ['parallel', 'neoj4_point']:
            if key in config_dict:
                value = config_dict[key].lower()
                config_dict[key] = value in ('true', '1', 'yes')
        
        # Convert string numbers to actual numbers
        for key in ['srid', 'batch_size', 'chunk_size', 'query_limit', 'query_offset', 
                    'thread_count', 'processor_count']:
            if key in config_dict and config_dict[key]:
                try:
                    config_dict[key] = int(config_dict[key])
                except ValueError:
                    pass  # Keep as string, let Pydantic handle the error
        
        for key in ['wntr_simulation_timestep_hours', 'wntr_simulation_length_hours']:
            if key in config_dict and config_dict[key]:
                try:
                    config_dict[key] = float(config_dict[key])
                except ValueError:
                    pass  # Keep as string, let Pydantic handle the error
        
        try:
            # Validate using Pydantic model
            validated_model = ConfigModel(**config_dict)
            # Convert to SimpleNamespace for backward compatibility
            self.validated_config = SimpleNamespace(**validated_model.model_dump())
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {str(e)}")
