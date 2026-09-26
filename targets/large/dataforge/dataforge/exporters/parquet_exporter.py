import pyarrow as pa
import pyarrow.parquet as pq
from typing import List, Dict, Any
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class ParquetExporter(BaseExporter):
    def __init__(self, file_path: str, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path

    def export(self, data: List[Dict[str, Any]]) -> None:
        if not data:
            return
        try:
            table = pa.Table.from_pylist(data)
            pq.write_table(table, self.file_path)
        except (pa.ArrowInvalid, OSError) as exc:
            raise ConnectorError(f"Failed to write Parquet to {self.file_path}: {exc}") from exc
