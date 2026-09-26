from typing import Callable, Dict, Type
from .exceptions import PluginNotFoundError

class PluginRegistry:
    """
    Central registry mapping plugin names to their implementation classes.
    Connectors, transformers, validators, and exporters all register here.
    """

    def __init__(self):
        self._connectors: Dict[str, Type] = {}
        self._transformers: Dict[str, Type] = {}
        self._validators: Dict[str, Type] = {}
        self._exporters: Dict[str, Type] = {}

    def register_connector(self, name: str) -> Callable:
        def decorator(cls: Type) -> Type:
            self._connectors[name] = cls
            return cls
        return decorator

    def register_transformer(self, name: str) -> Callable:
        def decorator(cls: Type) -> Type:
            self._transformers[name] = cls
            return cls
        return decorator

    def register_validator(self, name: str) -> Callable:
        def decorator(cls: Type) -> Type:
            self._validators[name] = cls
            return cls
        return decorator

    def register_exporter(self, name: str) -> Callable:
        def decorator(cls: Type) -> Type:
            self._exporters[name] = cls
            return cls
        return decorator

    def get_connector(self, name: str) -> Type:
        if name not in self._connectors:
            raise PluginNotFoundError(f"Connector '{name}' is not registered")
        return self._connectors[name]

    def get_transformer(self, name: str) -> Type:
        if name not in self._transformers:
            raise PluginNotFoundError(f"Transformer '{name}' is not registered")
        return self._transformers[name]

    def get_validator(self, name: str) -> Type:
        if name not in self._validators:
            raise PluginNotFoundError(f"Validator '{name}' is not registered")
        return self._validators[name]

    def get_exporter(self, name: str) -> Type:
        if name not in self._exporters:
            raise PluginNotFoundError(f"Exporter '{name}' is not registered")
        return self._exporters[name]


# Global singleton instance shared across the application
registry = PluginRegistry()
