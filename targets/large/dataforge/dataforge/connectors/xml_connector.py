import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class XMLConnector(BaseConnector):
    def __init__(self, file_path: str, record_tag: str = "record", **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.record_tag = record_tag

    def extract(self) -> List[Dict[str, Any]]:
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except (ET.ParseError, FileNotFoundError) as exc:
            raise ConnectorError(f"Failed to parse XML {self.file_path}: {exc}") from exc

        records = []
        for elem in root.iter(self.record_tag):
            record = {child.tag: child.text for child in elem}
            records.append(record)
        return records
