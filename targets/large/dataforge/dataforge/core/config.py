import os
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List
from .exceptions import PipelineConfigError

@dataclass
class StepConfig:
    plugin_type: str    # "connector" | "transformer" | "validator" | "exporter"
    plugin_name: str
    params: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PipelineConfig:
    name: str
    steps: List[StepConfig]
    max_retries: int = 3
    timeout_seconds: int = 300

    @classmethod
    def from_file(cls, path: str) -> "PipelineConfig":
        if not os.path.exists(path):
            raise PipelineConfigError(f"Config file not found: {path}")
        with open(path, "r") as f:
            raw = json.load(f)
        try:
            steps = [StepConfig(**s) for s in raw["steps"]]
            return cls(
                name=raw["name"],
                steps=steps,
                max_retries=raw.get("max_retries", 3),
                timeout_seconds=raw.get("timeout_seconds", 300),
            )
        except KeyError as exc:
            raise PipelineConfigError(f"Missing required field in config: {exc}")
