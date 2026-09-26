from typing import List, Dict, Any
from .base import BaseTransformer

class SortTransformer(BaseTransformer):
    """Sort records by a field, ascending or descending."""

    def __init__(self, field: str, descending: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.descending = descending

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return sorted(data, key=lambda row: row.get(self.field), reverse=self.descending)
