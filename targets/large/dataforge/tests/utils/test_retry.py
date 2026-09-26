import pytest
from dataforge.utils.retry import retry

def test_retry_succeeds_after_failures():
    attempts = {"count": 0}

    @retry(max_attempts=3, delay_seconds=0.01)
    def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError("not yet")
        return "success"

    assert flaky() == "success"
    assert attempts["count"] == 3

def test_retry_exhausts_and_raises():
    @retry(max_attempts=2, delay_seconds=0.01)
    def always_fails():
        raise ValueError("nope")

    with pytest.raises(ValueError):
        always_fails()
