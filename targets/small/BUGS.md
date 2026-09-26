# BUGS.md — Ground Truth (DO NOT expose to systems under test)

| # | File | Function | Category | Description |
|---|------|----------|----------|--------------|
| 1 | task_manager.py | `TaskManager.__init__` | Mutable Default Argument | `tasks: list = []` shares state across all instances. |
| 2 | task_manager.py | `sort_by_priority` | Logic Error | `reverse=False` sorts ascending instead of descending. |
| 3 | task_manager.py | `get_overdue_tasks` | Off-by-One / Boundary | `<=` marks tasks due today as overdue prematurely. |
| 4 | task_manager.py | `completion_rate` | Edge Case Failure | No guard for `total == 0` → ZeroDivisionError. |
| 5 | main.py | `sort_tasks_by_due_date` | Type Mismatch (Latent) | Sorts by `str(due_date)`; breaks silently on None/non-ISO dates. |

## Expected pytest Outcome
- `test_sort_by_priority_orders_high_first` → FAIL (Bug #2)
- `test_overdue_excludes_tasks_due_today` → FAIL (Bug #3)
- `test_completion_rate_empty_task_list` → ERROR (Bug #4)
- `test_mutable_default_argument_bug` → FAIL (Bug #1)
- All other tests → PASS
