from openpyxl import Workbook
from typing import List, Dict, Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class ExcelExporter(BaseExporter):
    def __init__(self, file_path: str, sheet_name: str = "Sheet1", **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.sheet_name = sheet_name

    def export(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            return
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = self.sheet_name
            headers = list(data[0].keys())
            ws.append(headers)
            for row in data:
                ws.append([row.get(h) for h in headers])
            wb.save(self.file_path)
        except OSError as exc:
            raise ConnectorError(f"Failed to write Excel file {self.file_path}: {exc}") from exc
