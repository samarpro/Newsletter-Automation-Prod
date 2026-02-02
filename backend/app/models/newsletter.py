"""
Newsletter database model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Newsletter(Base):
    """Newsletter model - stores created newsletters"""

    __tablename__ = "newsletters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    template_data = Column(JSON, nullable=True)  # Component tree structure
    html_content = Column(Text, nullable=True)  # Rendered HTML
    created_at = Column(DateTime, server_default=func.now())
    sent_at = Column(DateTime, nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    status = Column(String(50), default="draft")  # draft, scheduled, sending, sent, failed
    created_by = Column(String(100), default="admin")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    template = relationship("Template", back_populates="newsletters")
    newsletter_articles = relationship("NewsletterArticle", back_populates="newsletter", cascade="all, delete-orphan")
    email_sends = relationship("EmailSend", back_populates="newsletter")
    email_opens = relationship("EmailOpen", back_populates="newsletter")
    link_clicks = relationship("LinkClick", back_populates="newsletter")

    def __repr__(self):
        return f"<Newsletter(id={self.id}, title='{self.title}', status='{self.status}')>"
