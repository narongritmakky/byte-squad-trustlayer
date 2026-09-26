class DataForgeError(Exception):
    """Base exception for all DataForge errors."""

class ConnectorError(DataForgeError):
    """Raised when a connector fails to extract/load data."""

class TransformerError(DataForgeError):
    """Raised when a transformation step fails."""

class ValidationError(DataForgeError):
    """Raised when data fails validation rules."""

class PipelineConfigError(DataForgeError):
    """Raised when pipeline configuration is invalid."""

class PluginNotFoundError(DataForgeError):
    """Raised when a requested plugin is not registered."""
