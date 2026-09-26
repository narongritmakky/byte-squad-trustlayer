from datetime import date

from .exceptions import InvalidTaskDataError


def validate_title(title: str) -> str:
    if not isinstance(title, str):
        raise InvalidTaskDataError("Title must be a string.")
    stripped = title.strip()
    if not stripped:
        raise InvalidTaskDataError("Title cannot be empty.")
    if len(stripped) > 200:
        raise InvalidTaskDataError("Title cannot exceed 200 characters.")
    return stripped


def validate_priority(priority: int) -> int:
    if priority not in (1, 2, 3):
        raise InvalidTaskDataError("Priority must be 1 (LOW), 2 (MEDIUM), or 3 (HIGH).")
    return priority


def validate_due_date(due_date_str: str) -> date:
    try:
        return date.fromisoformat(due_date_str)
    except ValueError as exc:
        raise InvalidTaskDataError(f"Invalid date format: {due_date_str}. Use YYYY-MM-DD.") from exc
