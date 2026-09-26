class TaskFlowError(Exception):
    """Base exception for TaskFlow application."""


class TaskNotFoundError(TaskFlowError):
    def __init__(self, task_id: int):
        super().__init__(f"Task with id {task_id} was not found.")
        self.task_id = task_id


class InvalidTaskDataError(TaskFlowError):
    pass
