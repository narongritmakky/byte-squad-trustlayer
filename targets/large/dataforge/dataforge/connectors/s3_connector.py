import boto3
import json
from typing import Any
from botocore.exceptions import ClientError
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class S3Connector(BaseConnector):
    def __init__(self, bucket: str, key: str, region: str = "us-east-1", **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.key = key
        self.client = boto3.client("s3", region_name=region)

    def extract(self) -> Any:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=self.key)
            body = response["Body"].read().decode("utf-8")
            if self.key.endswith(".json"):
                return json.loads(body)
            return body
        except ClientError as exc:
            raise ConnectorError(f"S3 get_object failed for {self.key}: {exc}") from exc

    def load(self, data: Any) -> None:
        try:
            body = json.dumps(data) if not isinstance(data, str) else data
            self.client.put_object(Bucket=self.bucket, Key=self.key, Body=body.encode("utf-8"))
        except ClientError as exc:
            raise ConnectorError(f"S3 put_object failed for {self.key}: {exc}") from exc
