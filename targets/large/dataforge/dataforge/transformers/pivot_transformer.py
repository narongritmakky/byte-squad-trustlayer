from typing import List, Dict, Any
from collections import defaultdict
from .base import BaseTransformer

class PivotTransformer(BaseTransformer):
    """Pivot rows into columns: index_field becomes row key, column_field values become columns."""

    def __init__(self, index_field: str, column_field: str, value_field: str, **kwargs):
        super().__init__(**kwargs)
        self.index_field = index_field
        self.column_field = column_field
        self.value_field = value_field

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pivoted = defaultdict(dict)
        for row in data:
            idx = row.get(self.index_field)
            col = row.get(self.column_field)
            val = row.get(self.value_field)
            pivoted[idx][col] = val
            pivoted[idx][self.index_field] = idx
        return list(pivoted.values())
