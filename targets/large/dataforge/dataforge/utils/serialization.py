import json
from datetime import datetime, date
from typing import Any

def default_json_encoder(obj: Any) -> Any:
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def to_json(data: Any, indent: int = 2) -> str:
    return json.dumps(data, indent=indent, default=default_json_encoder)

def from_json(raw: str) -> Any:
    return json.loads(raw)
