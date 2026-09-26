from collections import defaultdict
from datetime import datetime
from typing import Dict, Any

# BUG #13 (Low): _counters เป็น module-level mutable dict ที่ถูก import และ
# แก้ไขจากหลาย thread พร้อมกัน (worker threads หลายตัวเรียก increment()
# ในเวลาเดียวกัน) โดยไม่มี lock ป้องกันเลย แม้ dict.__setitem__ ใน CPython
# จะ atomic ระดับหนึ่งเพราะ GIL แต่ "read-modify-write" แบบ counter[key] += 1
# ไม่ atomic — ถ้า thread สองตัวอ่านค่าเดิมพร้อมกันก่อนเขียนกลับ อาจทำให้
# เกิด "lost update" คือนับตกไป 1 ครั้ง (ยิ่งเจอบ่อยขึ้นเมื่อ worker เยอะขึ้น)
_counters: Dict[str, int] = defaultdict(int)
_timers: Dict[str, list] = defaultdict(list)

class MetricsCollector:
    """Lightweight in-process metrics tracking for pipeline runs."""

    def increment(self, metric_name: str, amount: int = 1) -> None:
        _counters[metric_name] += amount

    def record_duration(self, metric_name: str, duration_seconds: float) -> None:
        _timers[metric_name].append(duration_seconds)

    def get_counter(self, metric_name: str) -> int:
        return _counters.get(metric_name, 0)

    def get_avg_duration(self, metric_name: str) -> float:
        durations = _timers.get(metric_name, [])
        return sum(durations) / len(durations) if durations else 0.0

    def snapshot(self) -> Dict[str, Any]:
        return {
            "counters": dict(_counters),
            "avg_durations": {k: self.get_avg_duration(k) for k in _timers},
            "captured_at": datetime.utcnow().isoformat(),
        }
