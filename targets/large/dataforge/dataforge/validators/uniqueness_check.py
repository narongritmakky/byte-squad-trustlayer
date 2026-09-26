from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class UniquenessCheckValidator(BaseValidator):
    """Ensure a field's values are unique across all records."""

    def __init__(self, field: str, **kwargs):
        super().__init__(**kwargs)
        self.field = field

    def validate(self, data: List[Dict[str, Any]]) -> None:
        seen = set()
        for i, row in enumerate(data):
            val = row.get(self.field)
            if val in seen:
                raise ValidationError(f"Record {i}: duplicate value '{val}' for unique field '{self.field}'")
            seen.add(val)
