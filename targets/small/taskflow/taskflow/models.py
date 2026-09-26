from dataclasses import dataclass, field
from datetime import date
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    id: int
    title: str
    priority: Priority
    due_date: date
    completed: bool = False
    tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat(),
            "completed": self.completed,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            title=data["title"],
            priority=Priority(data["priority"]),
            due_date=date.fromisoformat(data["due_date"]),
            completed=data.get("completed", False),
            tags=data.get("tags", []),
        )
