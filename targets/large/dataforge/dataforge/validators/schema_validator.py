from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class SchemaValidator(BaseValidator):
    """Ensure each record has exactly the expected set of fields with correct types."""

    def __init__(self, expected_schema: Dict[str, type], **kwargs):
        super().__init__(**kwargs)
        self.expected_schema = expected_schema

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            for field, expected_type in self.expected_schema.items():
                if field not in row:
                    raise ValidationError(f"Record {i}: missing expected field '{field}'")
                val = row[field]
                if val is not None and not isinstance(val, expected_type):
                    raise ValidationError(
                        f"Record {i}: field '{field}' expected type {expected_type.__name__}, "
                        f"got {type(val).__name__}"
                    )
