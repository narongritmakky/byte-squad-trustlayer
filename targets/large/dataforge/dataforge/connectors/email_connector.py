import imaplib
import email
from typing import List, Dict, Any
from .base import BaseConnector
from ..core.exceptions import ConnectorError

class EmailConnector(BaseConnector):
    def __init__(self, host: str, username: str, password: str,
                 mailbox: str = "INBOX", limit: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.host, self.username, self.password = host, username, password
        self.mailbox, self.limit = mailbox, limit

    def extract(self) -> List[Dict[str, Any]]:
        results = []
        try:
            imap = imaplib.IMAP4_SSL(self.host)
            imap.login(self.username, self.password)
            imap.select(self.mailbox)
            _, message_ids = imap.search(None, "ALL")
            ids = message_ids[0].split()[-self.limit:]
            for msg_id in ids:
                _, data = imap.fetch(msg_id, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])
                results.append({"subject": msg["subject"], "from": msg["from"]})
            imap.close()
            imap.logout()
        except imaplib.IMAP4.error as exc:
            raise ConnectorError(f"IMAP fetch failed: {exc}") from exc
        return results
