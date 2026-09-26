import re
from typing import List, Dict, Any
from .base import BaseValidator
from ..core.exceptions import ValidationError

class RegexCheckValidator(BaseValidator):
    """Ensure a field's string value matches a regex pattern."""

    def __init__(self, field: str, pattern: str, **kwargs):
        super().__init__(**kwargs)
        self.field = field
        # BUG #8 (Low): pattern ที่ caller ส่งมา (เช่น r"^\d{5}$" สำหรับ zip code)
        # ถูกนำไปใช้กับ re.search() ด้านล่าง ไม่ใช่ re.match()/re.fullmatch()
        # ถ้า caller ลืมใส่ ^...$ เอง เช่นส่ง pattern=r"\d{5}" (ไม่ anchor)
        # validator จะ "ผ่าน" ค่าเช่น "abc12345xyz" เพราะ search() เจอ substring
        # ที่ match ตรงกลางได้ ทั้งที่ทั้ง field ไม่ใช่ zip code ที่ถูกต้องเลย
        self.pattern = re.compile(pattern)

    def validate(self, data: List[Dict[str, Any]]) -> None:
        for i, row in enumerate(data):
            val = row.get(self.field)
            if val is not None and not self.pattern.search(str(val)):
                raise ValidationError(f"Record {i}: {self.field}='{val}' does not match pattern")
