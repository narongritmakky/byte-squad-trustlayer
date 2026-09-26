from typing import List, Dict, Any, Optional
from datetime import datetime
import threading

class JobQueue:
    """
    In-memory job queue shared across worker threads.
    Jobs move through states: queued -> running -> completed/failed.
    """

    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def enqueue(self, job_id: str, pipeline_name: str) -> None:
        with self._lock:
            self._jobs[job_id] = {
                "pipeline_name": pipeline_name,
                "status": "queued",
                "enqueued_at": datetime.utcnow(),
            }

    def claim_next(self) -> Optional[str]:
        """
        Called by worker threads to atomically claim the next queued job.
        """
        # BUG #11 (High): Race condition — การหา job ที่ status=="queued" (read)
        # และการเปลี่ยนเป็น "running" (write) ไม่ได้อยู่ภายใต้ self._lock เดียวกัน
        # เป็น atomic operation เดียว มันคือ classic "check-then-act" ที่ถูกแยก
        # เป็นสองขั้นตอน ถ้ามี worker thread 2 ตัวเรียก claim_next() พร้อมกัน
        # ทั้งคู่อาจ "check" เห็น job เดียวกันเป็น queued ก่อนที่ตัวใดตัวหนึ่งจะ
        # ทัน "act" เปลี่ยนสถานะ ผลคือ job เดียวกันถูก 2 worker รันซ้อนกัน
        # (duplicate execution) — โดยเฉพาะเห็นชัดเวลามี concurrent workers สูง
        queued_ids = [jid for jid, job in self._jobs.items() if job["status"] == "queued"]
        if not queued_ids:
            return None

        job_id = queued_ids[0]
        with self._lock:
            self._jobs[job_id]["status"] = "running"
            self._jobs[job_id]["started_at"] = datetime.utcnow()
        return job_id

    def mark_completed(self, job_id: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "completed"
                self._jobs[job_id]["completed_at"] = datetime.utcnow()

    def mark_failed(self, job_id: str, error: str) -> None:
        with self._lock:
            if job_id in self._jobs:
                self._jobs[job_id]["status"] = "failed"
                self._jobs[job_id]["error"] = error

    def get_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._jobs.get(job_id)

    def list_jobs(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [{"job_id": jid, **job} for jid, job in self._jobs.items()]
