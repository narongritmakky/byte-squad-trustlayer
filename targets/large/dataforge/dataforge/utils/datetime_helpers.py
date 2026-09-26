from datetime import datetime, timezone

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def to_iso(dt: datetime) -> str:
    return dt.isoformat()

def parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)

def elapsed_seconds(start: datetime, end: datetime = None) -> float:
    end = end or utc_now()
    return (end - start).total_seconds()
