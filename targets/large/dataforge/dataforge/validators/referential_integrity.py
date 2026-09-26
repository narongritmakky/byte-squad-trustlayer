from typing import List, Dict, Any, Set
from .base import BaseValidator
from ..core.exceptions import ValidationError

class ReferentialIntegrityValidator(BaseValidator):
    """Ensure a foreign-key-style field references a value present in a known valid set."""

    def __init__(self, field: str, valid_values: Set[Any], **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.valid_values = valid_values

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            val = row.get(self.field)
            if val is not None and val not in self.valid_values:
                raise ValidationError(f"Record {i}: {self.field}='{val}' has no matching reference")
