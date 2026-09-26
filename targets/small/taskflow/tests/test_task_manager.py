from datetime import date

from taskflow.task_manager import TaskManager
from taskflow.storage import JSONStorage


class FakeStorage(JSONStorage):
    def __init__(self):
        self._tasks = []

    def load(self):
        return list(self._tasks)

    def save(self, tasks):
        self._tasks = list(tasks)


def test_add_task():
    manager = TaskManager(storage=FakeStorage(), tasks=[])
    task = manager.add_task("Write report", 2, "2026-12-01")
    assert task.title == "Write report"
    assert task.priority.value == 2


def test_complete_task():
    manager = TaskManager(storage=FakeStorage(), tasks=[])
    task = manager.add_task("Buy milk", 1, "2026-12-01")
    manager.complete_task(task.id)
    assert manager.get_task(task.id).completed is True


def test_sort_by_priority_orders_high_first():
    manager = TaskManager(storage=FakeStorage(), tasks=[])
    manager.add_task("Low", 1, "2026-12-01")
    manager.add_task("High", 3, "2026-12-01")
    manager.add_task("Medium", 2, "2026-12-01")
    ordered = manager.sort_by_priority()
    # NOTE: FAILS due to Bug #2 (reversed sort logic).
    assert [t.title for t in ordered] == ["High", "Medium", "Low"]


def test_overdue_excludes_tasks_due_today():
    manager = TaskManager(storage=FakeStorage(), tasks=[])
    today = date.today()
    manager.add_task("Due today", 2, today.isoformat())
    overdue = manager.get_overdue_tasks(as_of=today)
    # NOTE: FAILS due to Bug #3 (off-by-one boundary error).
    assert overdue == []


def test_completion_rate_empty_task_list():
    manager = TaskManager(storage=FakeStorage(), tasks=[])
    # NOTE: Raises ZeroDivisionError due to Bug #4.
    rate = manager.completion_rate()
    assert rate == 0.0


def test_mutable_default_argument_bug():
    manager_a = TaskManager()
    manager_a.add_task("Task A", 1, "2026-12-01")

    manager_b = TaskManager()
    # NOTE: FAILS due to Bug #1 — manager_b.tasks already contains
    # "Task A" because both instances share the same default list.
    assert manager_b.tasks == []
