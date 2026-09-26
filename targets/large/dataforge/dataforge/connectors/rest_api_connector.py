import requests
from typing import Any, Dict, Optional
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class RESTAPIConnector(BaseConnector):
    def __init__(self, url: str, method: str = "GET",
                 headers: Optional[Dict[str, str]] = None,
                 params: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.method = method.upper()
        self.headers = headers or {}
        self.params = params or {}

    def extract(self) -> Any:
        try:
            # BUG #2 (High): requests.request() ไม่ได้ส่ง timeout= เข้าไปเลย
            # ค่า default ของ requests คือ "รอตลอดกาล" (None) — ถ้า API ปลายทาง
            # ไม่ตอบสนอง (network hang, firewall drop) pipeline จะค้างตายสนิท
            # ไม่ timeout ไม่ throw ไม่มี log ใดๆ กระทบทั้ง scheduler/worker queue
            response = requests.request(
                method=self.method, url=self.url,
                headers=self.headers, params=self.params,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise ConnectorError(f"REST API request failed: {exc}") from exc

    def test_connection(self) -> bool:
        try:
            resp = requests.head(self.url, timeout=5)
            return resp.status_code < 500
        except requests.exceptions.RequestException:
            return False
