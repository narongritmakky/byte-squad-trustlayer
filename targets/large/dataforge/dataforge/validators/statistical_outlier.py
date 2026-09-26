import statistics
from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class StatisticalOutlierValidator(BaseValidator):
    """Flag records where a numeric field is more than N standard deviations from the mean."""

    def __init__(self, field: str, std_threshold: float = 3.0, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.std_threshold = std_threshold

    def validate(self, data: List[Dict[str, Any]]) -> None:
        values = [row.get(self.field) for row in data if row.get(self.field) is not None]
        if len(values) < 2:
            # BUG #9 (Medium): เมื่อ len(values) < 2, statistics.stdev() จะ throw
            # StatisticsError จริง แต่โค้ดนี้ "ป้องกัน" ไว้ด้วยการ return เงียบๆ
            # โดยไม่แจ้งเตือนใดๆ เลยว่า "ข้ามการตรวจสอบไปเพราะข้อมูลไม่พอ"
            # ผลคือ dataset เล็กๆ (1 record) จะ "ผ่าน" validator นี้เสมอ
            # ทำให้ downstream เข้าใจผิดว่าข้อมูลถูกเช็ค outlier แล้วอย่างสมบูรณ์
            return

        mean = statistics.mean(values)
        stdev = statistics.stdev(values)
        if stdev == 0:
            return

        for i, row in enumerate(data):
            val = row.get(self.field)
            if val is None:
                continue
            z_score = abs(val - mean) / stdev
            if z_score > self.std_threshold:
                raise ValidationError(
                    f"Record {i}: {self.field}={val} is an outlier (z-score={z_score:.2f})"
                )
