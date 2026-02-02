"""
Email tracking models for analytics
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class EmailSend(Base):
    """Track email sends"""

    __tablename__ = "email_sends"

    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id"), nullable=False, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False, index=True)
    sent_at = Column(DateTime, server_default=func.now(), index=True)
    status = Column(String(50), default="sent")  # sent, bounced, failed

    # Relationships
    newsletter = relationship("Newsletter", back_populates="email_sends")
    subscriber = relationship("Subscriber", back_populates="email_sends")

    def __repr__(self):
        return f"<EmailSend(id={self.id}, newsletter_id={self.newsletter_id}, subscriber_id={self.subscriber_id}, status='{self.status}')>"


class EmailOpen(Base):
    """Track email opens via tracking pixel"""

    __tablename__ = "email_opens"

    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id"), nullable=False, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False, index=True)
    opened_at = Column(DateTime, server_default=func.now(), index=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Relationships
    newsletter = relationship("Newsletter", back_populates="email_opens")
    subscriber = relationship("Subscriber", back_populates="email_opens")

    def __repr__(self):
        return f"<EmailOpen(id={self.id}, newsletter_id={self.newsletter_id}, subscriber_id={self.subscriber_id})>"


class LinkClick(Base):
    """Track link clicks via URL tracking"""

    __tablename__ = "link_clicks"

    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id"), nullable=False, index=True)
    subscriber_id = Column(Integer, ForeignKey("subscribers.id"), nullable=False, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True, index=True)
    original_url = Column(String(1000), nullable=False)
    clicked_at = Column(DateTime, server_default=func.now(), index=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(50), nullable=True)

    # Relationships
    newsletter = relationship("Newsletter", back_populates="link_clicks")
    subscriber = relationship("Subscriber", back_populates="link_clicks")
    article = relationship("Article", back_populates="link_clicks")

    def __repr__(self):
        return f"<LinkClick(id={self.id}, newsletter_id={self.newsletter_id}, subscriber_id={self.subscriber_id}, article_id={self.article_id})>"
