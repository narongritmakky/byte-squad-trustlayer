import pytest
from datetime import date

from taskflow.validators import validate_title, validate_priority, validate_due_date
from taskflow.exceptions import InvalidTaskDataError


def test_validate_title_strips_whitespace():
    assert validate_title("  Buy milk  ") == "Buy milk"


def test_validate_title_rejects_empty():
    with pytest.raises(InvalidTaskDataError):
        validate_title("   ")


def test_validate_priority_rejects_invalid():
    with pytest.raises(InvalidTaskDataError):
        validate_priority(5)


def test_validate_due_date_parses_iso():
    assert validate_due_date("2026-12-01") == date(2026, 12, 1)


def test_validate_due_date_rejects_bad_format():
    with pytest.raises(InvalidTaskDataError):
        validate_due_date("not-a-date")
