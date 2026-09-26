import csv
from typing import List, Dict, Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class CSVExporter(BaseExporter):
    def __init__(self, file_path: str, encoding: str = "utf-8", **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.encoding = encoding

    def export(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            return
        try:
            fieldnames = list(data[0].keys())
            with open(self.file_path, "w", encoding=self.encoding, newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except OSError as exc:
            raise ConnectorError(f"Failed to write CSV to {self.file_path}: {exc}") from exc
