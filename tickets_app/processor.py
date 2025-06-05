"""High level routines to fetch emails and update the database."""

import logging
from datetime import datetime

from . import config
from .db import Session, init_db, models
from .email_client import fetch_emails
from .ai_processor import analyze_email

logger = logging.getLogger(__name__)


def process_new_emails(limit: int | None = None) -> int:
    """Fetch new emails, analyze them and store information in the database.

    Parameters
    ----------
    limit: int
        Maximum number of emails to process in this call.

    Returns
    -------
    int
        Number of emails processed.
    """

    init_db()
    session = Session()
    processed = 0

    limit = limit or config.MAX_EMAILS
    logger.info("Fetching up to %s new emails", limit)

    for msg in fetch_emails(config.OUTLOOK_FOLDER)[:limit]:
        # skip if email already stored
        if session.query(models.Email).filter_by(entry_id=msg.entry_id).first():
            logger.debug("Email %s already processed", msg.entry_id)
            continue

        # analyze with OpenAI
        analysis = analyze_email(msg.body)
        if analysis.get("es_ticket") is False:
            logger.info("Email %s not identified as ticket", msg.entry_id)
            continue

        ticket_number = analysis.get("numero_de_ticket") or msg.subject
        ticket = session.query(models.Ticket).filter_by(number=ticket_number).first()
        if not ticket:
            ticket = models.Ticket(number=ticket_number, status="nuevo")
            session.add(ticket)
            session.commit()

        dest_dir = config.ATTACHMENTS_DIR / ticket.number
        dest_dir.mkdir(parents=True, exist_ok=True)

        email = models.Email(
            ticket_id=ticket.id,
            entry_id=msg.entry_id,
            sender=msg.sender,
            recipients=msg.recipients,
            subject=msg.subject,
            received=msg.received,
            body=msg.body,
            attachments_path=str(dest_dir),
        )
        session.add(email)
        session.commit()

        # register attachments and move them to the ticket directory
        for path in msg.attachments:
            dest = dest_dir / path.name
            try:
                path.rename(dest)
            except Exception:
                dest = path
            attachment = models.Attachment(
                ticket_id=ticket.id, path=str(dest), from_email=True
            )
            session.add(attachment)

        obs = models.Observation(
            ticket_id=ticket.id,
            email_id=email.id,
            summary=analysis.get("resumen"),
            next_step=analysis.get("proximo_paso"),
            urgency=analysis.get("urgencia"),
            closed=analysis.get("cerrado", False),
        )
        session.add(obs)

        # update ticket fields
        ticket.status = "cerrado" if obs.closed else "abierto"
        ticket.final_observation = obs.summary
        ticket.urgency = obs.urgency
        ticket.last_update = datetime.utcnow()

        session.commit()
        processed += 1

    logger.info("Processed %s emails", processed)
    return processed
