from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class StepIn(BaseModel):
    plugin_type: str
    plugin_name: str
    params: Dict[str, Any] = {}

class PipelineCreate(BaseModel):
    name: str
    steps: List[StepIn]
    max_retries: int = 3
    timeout_seconds: int = 300

class PipelineOut(BaseModel):
    name: str
    step_count: int

class RunOut(BaseModel):
    job_id: str
    pipeline_name: str
    status: str
    enqueued_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

class PluginInfo(BaseModel):
    plugin_type: str
    name: str
