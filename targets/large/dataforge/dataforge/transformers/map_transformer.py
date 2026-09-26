from typing import List, Dict, Any, Callable
from .base import BaseTransformer

class MapTransformer(BaseTransformer):
    """Apply a function to each record, e.g. add computed fields."""

    def __init__(self, fn: Callable[[Dict], Dict], **kwargs):
        super().__init__(**kwargs)
        self.fn = fn

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.fn(row) for row in data]
