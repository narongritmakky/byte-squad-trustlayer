import requests
import json
from typing import Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class WebhookExporter(BaseExporter):
    def __init__(self, url: str, headers: dict = None, **kwargs):
        super().__init__(**kwargs)
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}

    def export(self, data: Any) -> None:
        try:
            response = requests.post(
                self.url, json=data, headers=self.headers, timeout=30,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise ConnectorError(f"Webhook POST failed: {exc}") from exc
