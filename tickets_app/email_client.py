"""Module to interact with Outlook/Exchange and download new emails."""

import logging
from typing import List
from pathlib import Path
from datetime import datetime

try:
    import win32com.client  # type: ignore
except ImportError:  # not on Windows or library not installed
    win32com = None

from . import config

logger = logging.getLogger(__name__)

class EmailMessage:
    def __init__(
        self,
        entry_id: str,
        sender: str,
        recipients: str,
        subject: str,
        received: datetime,
        body: str,
        attachments: List[Path],
    ):
        self.entry_id = entry_id
        self.sender = sender
        self.recipients = recipients
        self.subject = subject
        self.received = received
        self.body = body
        self.attachments = attachments


def connect_outlook():
    if win32com is None:
        raise RuntimeError("win32com is not available. Outlook integration only works on Windows with pywin32 installed.")
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    return outlook


def fetch_emails(folder_name: str = None) -> List[EmailMessage]:
    folder_name = folder_name or config.OUTLOOK_FOLDER
    outlook = connect_outlook()
    inbox = outlook.GetDefaultFolder(6).Folders(folder_name)
    messages = []
    for item in inbox.Items:
        entry_id = item.EntryID
        attachments = []
        attach_dir = config.ATTACHMENTS_DIR / entry_id
        attach_dir.mkdir(parents=True, exist_ok=True)
        for att in item.Attachments:
            att_path = attach_dir / att.FileName
            att.SaveAsFile(str(att_path))
            attachments.append(att_path)
        msg = EmailMessage(
            entry_id=entry_id,
            sender=item.SenderEmailAddress,
            recipients=item.To,
            subject=item.Subject,
            received=item.ReceivedTime,
            body=item.Body,
            attachments=attachments,
        )
        messages.append(msg)
    return messages
