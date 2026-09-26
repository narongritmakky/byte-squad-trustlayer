from typing import List, Dict, Any
from .base import BaseTransformer

class RenameTransformer(BaseTransformer):
    """Rename fields according to a mapping {old_name: new_name}."""

    def __init__(self, mapping: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        result = []
        for row in data:
            new_row = {self.mapping.get(k, k): v for k, v in row.items()}
            result.append(new_row)
        return result
