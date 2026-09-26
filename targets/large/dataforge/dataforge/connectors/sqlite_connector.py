import sqlite3
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class SQLiteConnector(BaseConnector):
    def __init__(self, db_path: str, query: str, **kwargs):
        super().__init__(**kwargs)
        self.db_path = db_path
        self.query = query

    def extract(self) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(self.query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as exc:
            raise ConnectorError(f"SQLite query failed: {exc}") from exc
        finally:
            if conn:
                conn.close()
