from abc import ABC, abstractmethod
from typing import Any

class BaseConnector(ABC):
    """
    Abstract base class for all data source/sink connectors.
    Subclasses must implement extract(). Some also support load()
    for connectors that can act as both source and destination.
    """

    def __init__(self, **kwargs):
        self.config = kwargs

    @abstractmethod
    def extract(self) -> Any:
        """Pull data from the source and return it in a normalized format."""
        raise NotImplementedError

    def load(self, data: Any) -> None:
        """Optional: push data to the destination (not all connectors support this)."""
        raise NotImplementedError(f"{self.__class__.__name__} does not support load()")

    def test_connection(self) -> bool:
        """Optional health-check, overridden by connectors that support it."""
        return True
