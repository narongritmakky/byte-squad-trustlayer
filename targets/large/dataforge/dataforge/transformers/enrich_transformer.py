from typing import List, Dict, Any, Callable
from .base import BaseTransformer

class EnrichTransformer(BaseTransformer):
    """Add derived/computed fields to each record via a lookup function."""

    def __init__(self, target_field: str, source_fn: Callable[[Dict], Any], **kwargs):
        super().__init__(**kwargs)
        self.target_field = target_field
        self.source_fn = source_fn

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for row in data:
            row[self.target_field] = self.source_fn(row)
        return data
