from typing import List, Dict, Any
from .base import BaseTransformer

class JoinTransformer(BaseTransformer):
    """Inner join two lists of records on a shared key."""

    def __init__(self, right_data: List[Dict], left_key: str, right_key: str = None, **kwargs):
        super().__init__(**kwargs)
        self.right_data = right_data
        self.left_key = left_key
        self.right_key = right_key or left_key

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        right_index = {row.get(self.right_key): row for row in self.right_data}
        joined = []
        for left_row in data:
            match = right_index.get(left_row.get(self.left_key))
            if match:
                merged = {**left_row, **{k: v for k, v in match.items() if k != self.right_key}}
                joined.append(merged)
        return joined
