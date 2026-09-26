from typing import Callable, List
from .context import PipelineContext

class HookManager:
    """Lifecycle hooks: before/after each pipeline step, for logging/metrics/alerts."""

    def __init__(self):
        self._before_step: List[Callable] = []
        self._after_step: List[Callable] = []
        self._on_error: List[Callable] = []

    def on_before_step(self, fn: Callable) -> None:
        self._before_step.append(fn)

    def on_after_step(self, fn: Callable) -> None:
        self._after_step.append(fn)

    def on_error(self, fn: Callable) -> None:
        self._on_error.append(fn)

    def fire_before_step(self, step_name: str, context: PipelineContext) -> None:
        for fn in self._before_step:
            fn(step_name, context)

    def fire_after_step(self, step_name: str, context: PipelineContext) -> None:
        for fn in self._after_step:
            fn(step_name, context)

    def fire_error(self, step_name: str, context: PipelineContext, error: Exception) -> None:
        for fn in self._on_error:
            fn(step_name, context, error)
