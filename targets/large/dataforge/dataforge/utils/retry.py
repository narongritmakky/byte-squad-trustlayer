import time
from functools import wraps
from typing import Callable, Tuple, Type

def retry(max_attempts: int = 3, delay_seconds: float = 1.0,
          exceptions: Tuple[Type[Exception], ...] = (Exception,)) -> Callable:
    """Decorator: retry a function with fixed delay on specified exceptions."""

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        time.sleep(delay_seconds)
            raise last_exc
        return wrapper
    return decorator
