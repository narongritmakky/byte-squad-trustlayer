import pytest
from unittest.mock import patch, MagicMock
from dataforge.connectors.rest_api_connector import RESTAPIConnector

def test_extract_calls_requests_without_explicit_timeout():
    # ทดสอบ BUG #2: ยืนยันว่า requests.request() ถูกเรียกโดยไม่มี timeout kwarg
    connector = RESTAPIConnector(url="https://api.example.com/data")
    with patch("dataforge.connectors.rest_api_connector.requests.request") as mock_req:
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}
        mock_req.return_value = mock_response

        connector.extract()

        _, kwargs = mock_req.call_args
        assert "timeout" not in kwargs  # นี่คือหลักฐานของ BUG #2
