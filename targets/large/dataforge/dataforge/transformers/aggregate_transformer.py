from typing import List, Dict, Any
from collections import defaultdict
from .base import BaseTransformer
from ..core.exceptions import TransformerError

class AggregateTransformer(BaseTransformer):
    """Group by a key field and aggregate a numeric field (sum/avg/count/max/min)."""

    def __init__(self, group_by: str, agg_field: str, agg_func: str = "sum", **kwargs):
        super().__init__(**kwargs)
        self.group_by = group_by
        self.agg_field = agg_field
        self.agg_func = agg_func

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        groups = defaultdict(list)
        for row in data:
            groups[row.get(self.group_by)].append(row.get(self.agg_field))

        results = []
        for key, values in groups.items():
            # BUG #5 (Medium): ไม่ filter ค่า None ออกก่อนคำนวณ —
            # ถ้า field มีค่า missing/None ปนมา จะเจอ TypeError ตอน sum(),
            # หรือถ้าใช้ "count" จะนับ None รวมเข้าไปด้วย ทำให้ค่าเฉลี่ยผิดเพี้ยน
            # (ตัวหารรวม None ที่ไม่ควรถูกนับเข้าไปในชุดข้อมูลจริง)
            if self.agg_func == "sum":
                result = sum(values)
            elif self.agg_func == "avg":
                result = sum(values) / len(values)
            elif self.agg_func == "count":
                result = len(values)
            elif self.agg_func == "max":
                result = max(values)
            elif self.agg_func == "min":
                result = min(values)
            else:
                raise TransformerError(f"Unknown aggregation function: {self.agg_func}")
            results.append({self.group_by: key, f"{self.agg_field}_{self.agg_func}": result})
        return results
