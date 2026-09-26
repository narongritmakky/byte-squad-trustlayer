import redis
import json
from typing import Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class RedisConnector(BaseConnector):
    def __init__(self, host: str, port: int, key_pattern: str, db: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.key_pattern = key_pattern

    def extract(self) -> Any:
        try:
            keys = self.client.keys(self.key_pattern)
            return {k: self.client.get(k) for k in keys}
        except redis.RedisError as exc:
            raise ConnectorError(f"Redis extract failed: {exc}") from exc

    def load(self, data: dict) -> None:
        try:
            for k, v in data.items():
                value = json.dumps(v) if not isinstance(v, str) else v
                self.client.set(k, value)
        except redis.RedisError as exc:
            raise ConnectorError(f"Redis load failed: {exc}") from exc
