import time
import threading
from typing import Callable
from .job_queue import JobQueue
from ..core.exceptions import DataForgeError
from ..utils.logger import get_logger

logger = get_logger("dataforge.worker")

class Worker:
    """Background thread that continuously claims and executes jobs from the queue."""

    def __init__(self, queue: JobQueue, executor_fn: Callable[[str], None],
                 poll_interval: float = 1.0, max_retries: int = 3):
        self.queue = queue
        self.executor_fn = executor_fn
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self._running = False
        self._thread = None

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def _run_loop(self) -> None:
        while self._running:
            job_id = self.queue.claim_next()
            if job_id is None:
                time.sleep(self.poll_interval)
                continue
            self._execute_with_retry(job_id)

    def _execute_with_retry(self, job_id: str) -> None:
        attempts = 0
        while attempts < self.max_retries:
            try:
                self.executor_fn(job_id)
                self.queue.mark_completed(job_id)
                return
            except DataForgeError as exc:
                attempts += 1
                logger.warning(f"Job {job_id} failed (attempt {attempts}/{self.max_retries}): {exc}")
                # BUG #12 (Medium): retry ทันทีไม่มี backoff delay ระหว่างครั้ง
                # (ไม่มี time.sleep() ใดๆ ก่อน retry รอบต่อไป) ถ้า downstream
                # service ล่มชั่วคราว (เช่น DB connection pool เต็ม) worker
                # หลายตัวที่ retry พร้อมกันจะยิง request ซ้อนกันถี่มากจนกลาย
                # เป็น "thundering herd" ซ้ำเติมปัญหาที่ downstream ให้แย่ลงไปอีก
                # แทนที่จะให้เวลามันฟื้นตัว
        self.queue.mark_failed(job_id, f"Exceeded {self.max_retries} retries")
