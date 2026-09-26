from typing import List, Dict, Any, Callable
from .base import BaseValidator
from ..core.exceptions import ValidationError

class CustomRuleValidator(BaseValidator):
    """Run an arbitrary predicate function against each record."""

    def __init__(self, rule_fn: Callable[[Dict], bool], error_message: str = "Custom rule failed", **kwargs):
        super().__init__(**kwargs)
        self.rule_fn = rule_fn
        self.error_message = error_message

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            if not self.rule_fn(row):
                raise ValidationError(f"Record {i}: {self.error_message}")
