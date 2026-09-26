from typing import Callable, List
from ..core.context import PipelineContext
from .metrics_collector import MetricsCollector

class AlertManager:
    """Fires alert callbacks (e.g. Slack/email) when pipeline error thresholds are exceeded."""

    def __init__(self, error_threshold: int = 5):
        self.error_threshold = error_threshold
        self._alert_callbacks: List[Callable[[str], None]] = []
        self.metrics = MetricsCollector()

    def register_callback(self, fn: Callable[[str], None]) -> None:
        self._alert_callbacks.append(fn)

    def check_and_alert(self, context: PipelineContext) -> None:
        error_count = len(context.errors)
        self.metrics.increment(f"{context.pipeline_name}.errors", error_count)

        if error_count >= self.error_threshold:
            message = (
                f"Pipeline '{context.pipeline_name}' exceeded error threshold: "
                f"{error_count} errors (threshold={self.error_threshold})"
            )
            for callback in self._alert_callbacks:
                callback(message)
