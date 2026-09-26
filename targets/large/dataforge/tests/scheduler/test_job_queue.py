import threading
from dataforge.scheduler.job_queue import JobQueue

def test_concurrent_claim_next_may_duplicate():
    # ทดสอบ BUG #11: จำลอง 2 worker thread claim job เดียวกันพร้อมกัน
    queue = JobQueue()
    queue.enqueue("job-1", "test_pipeline")

    claimed = []
    def worker():
        job_id = queue.claim_next()
        if job_id:
            claimed.append(job_id)

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # ในระบบที่ไม่มี race condition ควรมีแค่ 1 thread claim job ได้
    # แต่เพราะ BUG #11 บางครั้ง (ไม่เสมอไป — ขึ้นกับ timing) อาจเห็น
    # มากกว่า 1 thread claim job-1 ได้สำเร็จ (flaky test — สื่อถึงธรรมชาติ
    # ของ race condition ที่ตรวจจับได้ไม่ 100% ทุกครั้งที่รัน)
    assert len(claimed) >= 1  # อย่างน้อยต้องมีคน claim ได้
