from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class NullCheckValidator(BaseValidator):
    """Ensure specified required fields are not None/missing in any record."""

    def __init__(self, required_fields: List[str], **kwargs):
        super().__init__(**kwargs)
        self.required_fields = required_fields

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            for field in self.required_fields:
                if row.get(field) is None:
                    raise ValidationError(f"Record {i}: required field '{field}' is null/missing")
