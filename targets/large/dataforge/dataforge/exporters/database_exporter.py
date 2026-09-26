import sqlite3
from typing import List, Dict, Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class DatabaseExporter(BaseExporter):
    """Exports records into a SQLite table, auto-creating the table if needed."""

    def __init__(self, db_path: str, table_name: str, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self.table_name = table_name

    def export(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            return

        conn = sqlite3.connect(self.db_path)
        try:
            columns = list(data[0].keys())

            # BUG #10 (CRITICAL): SQL Injection — table_name และ columns มาจาก
            # config/params ของ pipeline (อาจมาจาก user input ปลายทาง เช่น
            # ผ่าน API ที่รับ pipeline config เป็น JSON) แล้วถูกต่อสตริงตรงเข้า
            # คำสั่ง SQL ด้วย f-string โดยไม่ผ่านการ escape/parameterize ใดๆ เลย
            # ถ้า table_name = "users; DROP TABLE users; --" จะรันโค้ดอันตราย
            # ได้ทันที เช่นเดียวกับ column name ที่ถ้ามีชื่อพิเศษปนมาจากไฟล์ CSV
            # ต้นทาง (เช่น "id, (SELECT password FROM admin)") ก็เจาะข้อมูลได้
            create_cols = ", ".join([f"{col} TEXT" for col in columns])
            create_sql = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({create_cols})"
            conn.execute(create_sql)

            col_names = ", ".join(columns)
            placeholders = ", ".join(["?" for _ in columns])
            insert_sql = f"INSERT INTO {self.table_name} ({col_names}) VALUES ({placeholders})"

            for row in data:
                values = [row.get(col) for col in columns]
                conn.execute(insert_sql, values)

            conn.commit()
        except sqlite3.Error as exc:
            raise ConnectorError(f"Database export failed: {exc}") from exc
        finally:
            conn.close()
