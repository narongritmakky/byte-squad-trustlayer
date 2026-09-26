from fastapi import APIRouter, HTTPException
from ..schemas import RunOut
from ...scheduler.job_queue import JobQueue

router = APIRouter(prefix="/runs", tags=["runs"])
_queue = JobQueue()

@router.get("/{job_id}", response_model=RunOut)
def get_run_status(job_id: str):
    status = _queue.get_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return RunOut(job_id=job_id, **status)

@router.get("/", response_model=list[RunOut])
def list_runs():
    return [RunOut(**job) for job in _queue.list_jobs()]
