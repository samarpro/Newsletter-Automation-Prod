"""
Template database model
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Template(Base):
    """Template model - stores reusable newsletter templates"""

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String(500), nullable=True)
    template_json = Column(JSON, nullable=False)  # Component structure
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    newsletters = relationship("Newsletter", back_populates="template")

    def __repr__(self):
        return f"<Template(id={self.id}, name='{self.name}', is_default={self.is_default})>"
