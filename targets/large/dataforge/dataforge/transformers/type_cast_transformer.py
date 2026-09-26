from typing import List, Dict, Any
from .base import BaseTransformer

class TypeCastTransformer(BaseTransformer):
    """Cast a field to a target type (int, float, str, bool)."""

    CASTERS = {"int": int, "float": float, "str": str, "bool": bool}

    def __init__(self, field: str, target_type: str, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        self.target_type = target_type
        self.caster = self.CASTERS.get(target_type, str)

    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for row in data:
            try:
                row[self.field] = self.caster(row.get(self.field))
            except (ValueError, TypeError):
                # BUG #7 (Medium): ตรงนี้ตั้งใจ "จับ error แล้วเซ็ต None" เพื่อไม่ให้
                # pipeline ล้ม แต่ผลข้างเคียงคือข้อมูลเสีย (bad data) ถูกแปลงเป็น
                # None แบบเงียบๆ ไม่มี log, ไม่มี counter, ไม่มีทางรู้เลยว่ามี
                # กี่ record ที่ cast ไม่ผ่าน — downstream steps คิดว่า None
                # คือ "missing data" ปกติ ทั้งที่จริงคือ "data ผิด type" ตั้งแต่ต้น
                row[self.field] = None
        return data
