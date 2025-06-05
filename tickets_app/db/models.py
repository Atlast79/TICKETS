from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True, nullable=False)
    client = Column(String)
    status = Column(String)
    detail = Column(Text)
    last_update = Column(DateTime, default=datetime.utcnow)
    final_observation = Column(Text)
    urgency = Column(String)
    personal_notes = Column(Text)

    emails = relationship('Email', back_populates='ticket')
    observations = relationship('Observation', back_populates='ticket')
    attachments = relationship('Attachment', back_populates='ticket')

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    entry_id = Column(String, unique=True)
    sender = Column(String)
    recipients = Column(Text)
    subject = Column(String)
    received = Column(DateTime)
    body = Column(Text)
    attachments_path = Column(Text)

    ticket = relationship('Ticket', back_populates='emails')
    observations = relationship('Observation', back_populates='email')

class Observation(Base):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text)
    next_step = Column(Text)
    urgency = Column(String)
    closed = Column(Boolean, default=False)

    ticket = relationship('Ticket', back_populates='observations')
    email = relationship('Email', back_populates='observations')


class Attachment(Base):
    __tablename__ = 'attachments'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    path = Column(Text)
    from_email = Column(Boolean, default=True)

    ticket = relationship('Ticket', back_populates='attachments')
