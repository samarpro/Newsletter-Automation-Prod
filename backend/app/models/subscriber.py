"""
Subscriber database model
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import secrets


class Subscriber(Base):
    """Subscriber model - stores newsletter subscribers"""

    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    subscribed_at = Column(DateTime, server_default=func.now())
    unsubscribed_at = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True, index=True)
    unsubscribe_token = Column(String(100), unique=True, default=lambda: secrets.token_urlsafe(32))
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    email_sends = relationship("EmailSend", back_populates="subscriber")
    email_opens = relationship("EmailOpen", back_populates="subscriber")
    link_clicks = relationship("LinkClick", back_populates="subscriber")

    def __repr__(self):
        return f"<Subscriber(id={self.id}, email='{self.email}', active={self.active})>"
