from typing import List, Dict, Any
from .base import BaseTransformer

class WindowTransformer(BaseTransformer):
    """Compute a rolling window aggregate (e.g. moving average) over a sorted field."""

    def __init__(self, field: str, window_size: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.window_size = window_size

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        values = [row.get(self.field, 0) for row in data]
        for i, row in enumerate(data):
            start = max(0, i - self.window_size + 1)
            window = values[start:i + 1]
            row[f"{self.field}_rolling_avg"] = sum(window) / len(window)
        return data
