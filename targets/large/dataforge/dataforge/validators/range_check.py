from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class RangeCheckValidator(BaseValidator):
    """Ensure a numeric field's value falls within [min_value, max_value]."""

    def __init__(self, field: str, min_value: float = None, max_value: float = None, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            val = row.get(self.field)
            if val is None:
                continue
            if self.min_value is not None and val < self.min_value:
                raise ValidationError(f"Record {i}: {self.field}={val} is below minimum {self.min_value}")
            if self.max_value is not None and val > self.max_value:
                raise ValidationError(f"Record {i}: {self.field}={val} exceeds maximum {self.max_value}")
