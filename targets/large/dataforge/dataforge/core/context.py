from typing import Any, Dict
from datetime import datetime

class PipelineContext:
    """
    Carries mutable state (data + metadata) as it flows through
    connector -> transformers -> validators -> exporter.
    """

    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.data: Any = None
        self.metadata: Dict[str, Any] = {}
        self.started_at = datetime.utcnow()
        self.errors: list = []

    def set_data(self, data: Any) -> None:
        self.data = data

    def add_error(self, step_name: str, error: Exception) -> None:
        self.errors.append({"step": step_name, "error": str(error), "type": type(error).__name__})

    def has_errors(self) -> bool:
        return len(self.errors) > 0
