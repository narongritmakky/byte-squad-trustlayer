from abc import ABC, abstractmethod
from typing import Any

class BaseValidator(ABC):
    """Abstract base class for all data validation rules."""

    def __init__(self, **kwargs):
        self.config = kwargs

    @abstractmethod
    def validate(self, data: Any) -> None:
        """Raise ValidationError if data fails the rule. Return None if valid."""
        raise NotImplementedError
