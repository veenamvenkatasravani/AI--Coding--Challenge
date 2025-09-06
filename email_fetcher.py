import os
import email
import imaplib
import pandas as pd
from dotenv import load_dotenv

KEYWORDS = {"support", "query", "request", "help"}

load_dotenv()

class EmailFetcher:
    def __init__(self, source: str = "csv", csv_path: str = "sample_emails.csv"):
        self.source = source
        self.csv_path = csv_path

    def fetch(self):
        if self.source == "csv":
            df = pd.read_csv(self.csv_path)
            return df
        elif self.source == "imap":
            host = os.getenv("IMAP_HOST")
            user = os.getenv("IMAP_USER")
            pwd  = os.getenv("IMAP_PASSWORD")
            folder = os.getenv("IMAP_FOLDER", "INBOX")
            m = imaplib.IMAP4_SSL(host)
            m.login(user, pwd)
            m.select(folder)
            typ, data = m.search(None, 'ALL')
            rows = []
            for num in data[0].split():
                typ, msg_data = m.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                subject = msg.get('Subject', '')
                sender = email.utils.parseaddr(msg.get('From'))[1]
                date = msg.get('Date', '')
                body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body += part.get_payload(decode=True).decode(errors='ignore')
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                rows.append({"sender": sender, "subject": subject, "body": body, "date": date})
            m.close(); m.logout()
            return pd.DataFrame(rows)
        else:
            raise ValueError("Unknown source")

    def filter_support(self, df: pd.DataFrame) -> pd.DataFrame:
        mask = df['subject'].fillna('').str.lower().apply(
            lambda s: any(k in s for k in KEYWORDS)
        )
        return df[mask].copy().reset_index(drop=True)
