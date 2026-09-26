import csv
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class CSVConnector(BaseConnector):
    def __init__(self, file_path: str, delimiter: str = ",", encoding: str = "utf-8", **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding

    def extract(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding=self.encoding, newline="") as f:
                # BUG #4 (Low): self.delimiter ถูกรับเข้ามาใน __init__ และมีอยู่จริง
                # แต่ csv.DictReader ด้านล่างไม่ได้ส่ง delimiter=self.delimiter เข้าไป
                # เลย — ผลคือถ้าไฟล์เป็น TSV หรือ semicolon-separated จะ parse ผิด
                # โดยไม่ error ให้เห็น (คอลัมน์ทั้งหมดรวมกันเป็น field เดียว)
                reader = csv.DictReader(f)
                return [row for row in reader]
        except FileNotFoundError as exc:
            raise ConnectorError(f"CSV file not found: {self.file_path}") from exc
        except csv.Error as exc:
            raise ConnectorError(f"Failed to parse CSV: {exc}") from exc

    def load(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            return
        fieldnames = list(data[0].keys())
        with open(self.file_path, "w", encoding=self.encoding, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
