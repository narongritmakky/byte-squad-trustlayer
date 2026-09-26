from abc import ABC, abstractmethod
from typing import Any

class BaseExporter(ABC):
    """Abstract base class for all data export/sink destinations."""

    def __init__(self, **kwargs):
        self.config = kwargs

    @abstractmethod
    def export(self, data: Any) -> None:
        """Write data to the destination."""
        raise NotImplementedError
