import pymysql
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class MySQLConnector(BaseConnector):
    def __init__(self, host: str, port: int, database: str,
                 user: str, password: str, query: str, **kwargs):
        super().__init__(**kwargs)
        self.host, self.port, self.database = host, port, database
        self.user, self.password, self.query = user, password, query

    def extract(self) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host, port=self.port, db=self.database,
                user=self.user, password=self.password,
                cursorclass=pymysql.cursors.DictCursor,
            )
            with conn.cursor() as cursor:
                cursor.execute(self.query)
                return cursor.fetchall()
        except pymysql.MySQLError as exc:
            raise ConnectorError(f"MySQL query failed: {exc}") from exc
        finally:
            if conn:
                conn.close()
