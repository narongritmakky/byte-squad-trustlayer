import psycopg2
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class PostgresConnector(BaseConnector):
    def __init__(self, host: str, port: int, database: str,
                 user: str, password: str, query: str, **kwargs):
        super().__init__(**kwargs)
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.query = query

    def _connect(self):
        return psycopg2.connect(
            host=self.host, port=self.port, dbname=self.database,
            user=self.user, password=self.password,
        )

    def extract(self) -> List[Dict[str, Any]]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(self.query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        # BUG #3 (Medium): ไม่มี try/finally ครอบตั้งแต่ cursor.execute() —
        # ถ้า query ผิด syntax หรือ table ไม่มีจริง exception จะ throw ออกไปเลย
        # โดย conn/cursor ไม่ถูก close() เลย ทำให้ connection ค้างอยู่ใน Postgres
        # (เห็นได้จาก pg_stat_activity) จนกว่า connection pool/timeout จะเคลียร์เอง
        # เรียกใช้บ่อยๆ ใน loop จะทำให้ pool หมดและ service อื่นต่อ DB ไม่ได้
        cursor.close()
        conn.close()
        return [dict(zip(columns, row)) for row in rows]

    def test_connection(self) -> bool:
        try:
            conn = self._connect()
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False
