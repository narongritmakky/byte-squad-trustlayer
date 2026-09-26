from typing import List, Dict, Any, Callable
from .base import BaseTransformer
from ..core.exceptions import TransformerError

class FilterTransformer(BaseTransformer):
    """Keep only records where field == value, or where a custom predicate holds."""

    def __init__(self, field: str = None, value: Any = None,
                 predicate: Callable[[Dict], bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.value = value
        self.predicate = predicate

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not isinstance(data, list):
            raise TransformerError("FilterTransformer expects a list of records")

        if self.predicate:
            return [row for row in data if self.predicate(row)]
        if self.field is not None:
            return [row for row in data if row.get(self.field) == self.value]
        return data
