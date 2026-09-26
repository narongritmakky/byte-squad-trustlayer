from croniter import croniter
from datetime import datetime
from typing import Dict, Callable

class CronScheduler:
    """Maps cron expressions to pipeline trigger callbacks and computes next run times."""

    def __init__(self):
        self._schedules: Dict[str, str] = {}
        self._callbacks: Dict[str, Callable] = {}

    def add_schedule(self, name: str, cron_expr: str, callback: Callable) -> None:
        if not croniter.is_valid(cron_expr):
            raise ValueError(f"Invalid cron expression: {cron_expr}")
        self._schedules[name] = cron_expr
        self._callbacks[name] = callback

    def get_next_run(self, name: str, base_time: datetime = None) -> datetime:
        base_time = base_time or datetime.utcnow()
        cron_expr = self._schedules.get(name)
        if not cron_expr:
            raise KeyError(f"No schedule registered for '{name}'")
        itr = croniter(cron_expr, base_time)
        return itr.get_next(datetime)

    def due_schedules(self, now: datetime = None) -> list:
        now = now or datetime.utcnow()
        due = []
        for name, cron_expr in self._schedules.items():
            itr = croniter(cron_expr, now)
            prev_run = itr.get_prev(datetime)
            if (now - prev_run).total_seconds() < 60:
                due.append(name)
        return due

    def trigger(self, name: str) -> None:
        callback = self._callbacks.get(name)
        if callback:
            callback()
