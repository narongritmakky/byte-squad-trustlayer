import json
from pathlib import Path
from typing import List

from .models import Task


class JSONStorage:
    """Persists tasks to a JSON file on disk."""

    def __init__(self, filepath: str = "tasks.json"):
        self.filepath = Path(filepath)

    def load(self) -> List[Task]:
        if not self.filepath.exists():
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Task.from_dict(item) for item in raw]

    def save(self, tasks: List[Task]) -> None:
        data = [task.to_dict() for task in tasks]
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
