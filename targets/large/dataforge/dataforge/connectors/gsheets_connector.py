import gspread
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class GSheetsConnector(BaseConnector):
    def __init__(self, credentials_path: str, spreadsheet_id: str,
                 worksheet_name: str, **kwargs):
        super().__init__(**kwargs)
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name

    def extract(self) -> List[Dict[str, Any]]:
        try:
            gc = gspread.service_account(filename=self.credentials_path)
            sheet = gc.open_by_key(self.spreadsheet_id)
            worksheet = sheet.worksheet(self.worksheet_name)
            return worksheet.get_all_records()
        except gspread.exceptions.GSpreadException as exc:
            raise ConnectorError(f"Google Sheets read failed: {exc}") from exc
