import json
from typing import Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class JSONExporter(BaseExporter):
    def __init__(self, file_path: str, indent: int = 2, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.indent = indent

    def export(self, data: Any) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=self.indent, default=str)
        except OSError as exc:
            raise ConnectorError(f"Failed to write JSON to {self.file_path}: {exc}") from exc
