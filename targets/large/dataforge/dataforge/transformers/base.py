from abc import ABC, abstractmethod
from typing import Any

class BaseTransformer(ABC):
    """Abstract base class for all data transformation steps."""

    def __init__(self, **kwargs):
        self.config = kwargs

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Take input data and return transformed data."""
        raise NotImplementedError
