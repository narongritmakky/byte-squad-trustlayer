import json
from typing import Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class JSONConnector(BaseConnector):
    def __init__(self, file_path: str, encoding: str = "utf-8", **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.encoding = encoding

    def extract(self) -> Any:
        try:
            with open(self.file_path, "r", encoding=self.encoding) as f:
                return json.load(f)
        except FileNotFoundError as exc:
            raise ConnectorError(f"JSON file not found: {self.file_path}") from exc
        except json.JSONDecodeError as exc:
            raise ConnectorError(f"Invalid JSON in {self.file_path}: {exc}") from exc

    def load(self, data: Any) -> None:
        with open(self.file_path, "w", encoding=self.encoding) as f:
            json.dump(data, f, indent=2, default=str)
