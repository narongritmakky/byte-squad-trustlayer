import argparse
import sys

from .task_manager import TaskManager
from .exceptions import TaskFlowError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskflow", description="A simple CLI task manager.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task.")
    add_parser.add_argument("title", type=str)
    add_parser.add_argument("--priority", type=int, default=2, choices=[1, 2, 3])
    add_parser.add_argument("--due", type=str, required=True, help="YYYY-MM-DD")

    list_parser = subparsers.add_parser("list", help="List tasks.")
    list_parser.add_argument("--all", action="store_true", help="Include completed tasks.")
    list_parser.add_argument("--sort-by-due", action="store_true")

    complete_parser = subparsers.add_parser("complete", help="Mark a task complete.")
    complete_parser.add_argument("task_id", type=int)

    remove_parser = subparsers.add_parser("remove", help="Remove a task.")
    remove_parser.add_argument("task_id", type=int)

    subparsers.add_parser("overdue", help="Show overdue tasks.")
    subparsers.add_parser("stats", help="Show completion statistics.")

    return parser


def sort_tasks_by_due_date(tasks):
    # BUG #5 — Type Mismatch (Latent):
    # Sorting by `str(due_date)` instead of the `date` object works
    # TODAY only because ISO strings happen to sort correctly. It breaks
    # silently the moment `due_date` is ever None or non-ISO formatted —
    # no error is raised, tasks just get misordered.
    return sorted(tasks, key=lambda t: str(t.due_date))


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    manager = TaskManager()
    manager.load()

    try:
        if args.command == "add":
            task = manager.add_task(args.title, args.priority, args.due)
            print(f"Added task #{task.id}: {task.title}")

        elif args.command == "list":
            tasks = manager.list_tasks(include_completed=args.all)
            if args.sort_by_due:
                tasks = sort_tasks_by_due_date(tasks)
            for t in tasks:
                status = "x" if t.completed else " "
                print(f"[{status}] #{t.id} {t.title} (P{t.priority.value}, due {t.due_date})")

        elif args.command == "complete":
            manager.complete_task(args.task_id)
            print(f"Task #{args.task_id} marked complete.")

        elif args.command == "remove":
            manager.remove_task(args.task_id)
            print(f"Task #{args.task_id} removed.")

        elif args.command == "overdue":
            for t in manager.get_overdue_tasks():
                print(f"[OVERDUE] #{t.id} {t.title} (due {t.due_date})")

        elif args.command == "stats":
            rate = manager.completion_rate()
            print(f"Completion rate: {rate:.1f}%")

    except TaskFlowError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        manager.save()

    return 0


if __name__ == "__main__":
    sys.exit(main())
