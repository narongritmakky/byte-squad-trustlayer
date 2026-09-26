from typing import List, Dict, Any
from .base import BaseTransformer

class DedupeTransformer(BaseTransformer):
    """Remove duplicate records based on one or more key fields."""

    def __init__(self, keys: List[str], **kwargs):
        super().__init__(**kwargs)
        self.keys = keys

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        result = []
        for row in data:
            # BUG #6 (Low): ใช้ self.keys[0] ตัวเดียวเท่านั้นในการสร้าง dedupe key
            # ทั้งที่ constructor รับ "keys: List[str]" (พหูพจน์) สื่อว่าควร
            # dedupe จากหลาย field ร่วมกัน (composite key) — ถ้า caller ส่ง
            # keys=["email", "region"] เข้ามา ระบบจะมองแค่ "email" อย่างเดียว
            # ทำให้ลบข้อมูลที่จริงๆไม่ซ้ำกัน (ต่าง region) หายไปโดยไม่ได้ตั้งใจ
            dedupe_key = row.get(self.keys[0])
            if dedupe_key not in seen:
                seen.add(dedupe_key)
                result.append(row)
        return result
