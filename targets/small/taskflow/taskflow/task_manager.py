from datetime import date
from typing import List, Optional

from .models import Task, Priority
from .storage import JSONStorage
from .exceptions import TaskNotFoundError
from .validators import validate_title, validate_priority, validate_due_date


class TaskManager:
    def __init__(self, storage: Optional[JSONStorage] = None, tasks: list = []):
        # BUG #1 — Mutable Default Argument:
        # `tasks: list = []` is evaluated ONCE at function definition time.
        # Every TaskManager created without an explicit `tasks=` argument
        # shares the SAME list object, leaking state across instances.
        self.storage = storage or JSONStorage()
        self.tasks: List[Task] = tasks
        self._next_id = (max((t.id for t in self.tasks), default=0)) + 1

    def add_task(self, title: str, priority: int, due_date_str: str) -> Task:
        clean_title = validate_title(title)
        clean_priority = validate_priority(priority)
        clean_due_date = validate_due_date(due_date_str)

        task = Task(
            id=self._next_id,
            title=clean_title,
            priority=Priority(clean_priority),
            due_date=clean_due_date,
        )
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def complete_task(self, task_id: int) -> Task:
        task = self.get_task(task_id)
        task.completed = True
        return task

    def remove_task(self, task_id: int) -> None:
        task = self.get_task(task_id)
        self.tasks.remove(task)

    def list_tasks(self, include_completed: bool = True) -> List[Task]:
        if include_completed:
            return list(self.tasks)
        return [t for t in self.tasks if not t.completed]

    def sort_by_priority(self) -> List[Task]:
        # BUG #2 — Logic Error:
        # HIGH priority (value 3) should appear FIRST, but `reverse=False`
        # sorts ascending, putting LOW priority tasks on top instead.
        return sorted(self.tasks, key=lambda t: t.priority.value, reverse=False)

    def get_overdue_tasks(self, as_of: Optional[date] = None) -> List[Task]:
        as_of = as_of or date.today()
        # BUG #3 — Off-by-One / Boundary Error:
        # Using `<=` instead of `<` marks a task due exactly TODAY as
        # "overdue," when it should still be considered on-time.
        return [t for t in self.tasks if not t.completed and t.due_date <= as_of]

    def completion_rate(self) -> float:
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        # BUG #4 — Edge Case Failure:
        # No guard for `total == 0`, causing ZeroDivisionError for a
        # brand-new user with no tasks yet.
        return (completed / total) * 100

    def find_by_tag(self, tag: str) -> List[Task]:
        return [t for t in self.tasks if tag in t.tags]

    def save(self) -> None:
        self.storage.save(self.tasks)

    def load(self) -> None:
        self.tasks = self.storage.load()
        self._next_id = (max((t.id for t in self.tasks), default=0)) + 1
