from typing import List, Dict, Any
from .base import BaseTransformer

class NormalizeTransformer(BaseTransformer):
    """Normalize numeric field values to a 0-1 range (min-max scaling)."""

    def __init__(self, field: str, **kwargs):
        super().__init__(**kwargs)
        self.field = field

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        values = [row.get(self.field) for row in data if row.get(self.field) is not None]
        if not values:
            return data
        min_val, max_val = min(values), max(values)
        span = max_val - min_val if max_val != min_val else 1

        for row in data:
            val = row.get(self.field)
            if val is not None:
                row[f"{self.field}_normalized"] = (val - min_val) / span
        return data
