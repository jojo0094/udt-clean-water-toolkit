from pydantic import BaseModel
from typing import Optional

class GenerateSyntheticNetworkResponse(BaseModel):
    status: str
    message: str
    pipes_created: int
    hydrants_created: int
    valves_created: int
    flow_records_created: int

class HealthCheckResponse(BaseModel):
    status: str
    message: str
