from kafka import KafkaConsumer, KafkaProducer
import json
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class KafkaConnector(BaseConnector):
    def __init__(self, bootstrap_servers: str, topic: str,
                 max_messages: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.max_messages = max_messages

    def extract(self) -> List[Dict[str, Any]]:
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            auto_offset_reset="earliest",
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        messages = []
        try:
            for msg in consumer:
                messages.append(msg.value)
                if len(messages) >= self.max_messages:
                    break
        finally:
            consumer.close()
        return messages

    def load(self, data: List[Dict[str, Any]]) -> None:
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        try:
            for record in data:
                producer.send(self.topic, value=record)
            producer.flush()
        finally:
            producer.close()
