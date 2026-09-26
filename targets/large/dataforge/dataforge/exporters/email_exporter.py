import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from .base import BaseExporter
from ..core.exceptions import ConnectorError

class EmailExporter(BaseExporter):
    def __init__(self, smtp_host: str, smtp_port: int, sender: str,
                 recipients: List[str], subject: str, **kwargs):
        super().__init__(**kwargs)
        self.smtp_host, self.smtp_port = smtp_host, smtp_port
        self.sender, self.recipients, self.subject = sender, recipients, subject

    def export(self, data: str) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = ", ".join(self.recipients)
        msg["Subject"] = self.subject
        msg.attach(MIMEText(str(data), "plain"))

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=30) as server:
                server.send_message(msg)
        except smtplib.SMTPException as exc:
            raise ConnectorError(f"Failed to send email: {exc}") from exc
