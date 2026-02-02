"""
Newsletter-Article junction table
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class NewsletterArticle(Base):
    """Junction table for newsletters and articles"""

    __tablename__ = "newsletter_articles"

    id = Column(Integer, primary_key=True, index=True)
    newsletter_id = Column(Integer, ForeignKey("newsletters.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    position = Column(Integer, default=0)  # Display order in newsletter

    # Relationships
    newsletter = relationship("Newsletter", back_populates="newsletter_articles")
    article = relationship("Article", back_populates="newsletter_articles")

    def __repr__(self):
        return f"<NewsletterArticle(newsletter_id={self.newsletter_id}, article_id={self.article_id}, position={self.position})>"
