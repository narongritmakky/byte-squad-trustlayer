import ftplib
from io import BytesIO
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class FTPConnector(BaseConnector):
    def __init__(self, host: str, username: str, password: str,
                 remote_path: str, port: int = 21, **kwargs):
        super().__init__(**kwargs)
        self.host, self.port = host, port
        self.username, self.password = username, password
        self.remote_path = remote_path

    def extract(self) -> bytes:
        buffer = BytesIO()
        try:
            with ftplib.FTP() as ftp:
                ftp.connect(self.host, self.port, timeout=30)
                ftp.login(self.username, self.password)
                ftp.retrbinary(f"RETR {self.remote_path}", buffer.write)
        except ftplib.all_errors as exc:
            raise ConnectorError(f"FTP retrieval failed for {self.remote_path}: {exc}") from exc
        return buffer.getvalue()
