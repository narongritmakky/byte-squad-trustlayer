from typing import List, Dict, Any
from .base import BaseTransformer

class SchemaMapTransformer(BaseTransformer):
    """Restrict/reorder output fields to match a target schema, filling missing fields with None."""

    def __init__(self, target_fields: List[str], **kwargs):
        super().__init__(**kwargs)
        self.target_fields = target_fields

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [{field: row.get(field) for field in self.target_fields} for row in data]
