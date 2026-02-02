"""
Article database model
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Article(Base):
    """Article model - stores scraped articles"""

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    link = Column(String(1000), unique=True, nullable=False, index=True)
    categories = Column(JSON)  # Store as JSON array
    published = Column(DateTime, nullable=True)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Full scraped content
    ai_content = Column(Text, nullable=True)  # AI-processed content
    scraped_at = Column(DateTime, server_default=func.now())
    status = Column(String(50), default="draft")  # draft, selected, published, archived
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    newsletter_articles = relationship("NewsletterArticle", back_populates="article")
    link_clicks = relationship("LinkClick", back_populates="article")

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title[:50]}...')>"
