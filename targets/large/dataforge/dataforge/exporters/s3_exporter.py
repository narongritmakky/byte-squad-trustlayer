import boto3
import json
from typing import Any
from botocore.exceptions import ClientError
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class S3Exporter(BaseExporter):
    def __init__(self, bucket: str, key: str, region: str = "us-east-1", **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.client = boto3.client("s3", region_name=region)

    def export(self, data: Any) -> None:
        try:
            body = json.dumps(data, default=str) if not isinstance(data, str) else data
            self.client.put_object(Bucket=self.bucket, Key=self.key, Body=body.encode("utf-8"))
        except ClientError as exc:
            raise ConnectorError(f"S3 export failed for {self.key}: {exc}") from exc
