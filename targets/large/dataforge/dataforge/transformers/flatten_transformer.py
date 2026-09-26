from typing import List, Dict, Any
from .base import BaseTransformer

class FlattenTransformer(BaseTransformer):
    """Flatten nested dicts into dot-notation keys, e.g. {'a': {'b': 1}} -> {'a.b': 1}."""

    def __init__(self, separator: str = ".", **kwargs):
        super().__init__(**kwargs)
        self.separator = separator

    def _flatten(self, obj: Dict, prefix: str = "") -> Dict:
        flat = {}
        for k, v in obj.items():
            new_key = f"{prefix}{self.separator}{k}" if prefix else k
            if isinstance(v, dict):
                flat.update(self._flatten(v, new_key))
            else:
                flat[new_key] = v
        return flat

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self._flatten(row) for row in data]
