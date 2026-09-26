from elasticsearch import Elasticsearch
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class ElasticsearchConnector(BaseConnector):
    def __init__(self, hosts: List[str], index: str, query: Dict = None, size: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.client = Elasticsearch(hosts)
        self.index = index
        self.query = query or {"match_all": {}}
        self.size = size

    def extract(self) -> List[Dict[str, Any]]:
        try:
            response = self.client.search(
                index=self.index, query=self.query, size=self.size,
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as exc:
            raise ConnectorError(f"Elasticsearch query failed: {exc}") from exc
