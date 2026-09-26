import hashlib
import json

def hash_record(record: dict) -> str:
    """Compute a deterministic hash for a record, useful for dedup/change detection."""
    serialized = json.dumps(record, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

def hash_string(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()
