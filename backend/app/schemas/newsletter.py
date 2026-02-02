"""
Newsletter Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class NewsletterBase(BaseModel):
    """Base newsletter schema"""

    title: str
    subject: str
    template_id: Optional[int] = None
    template_data: Optional[Dict[str, Any]] = None
    status: str = "draft"


class NewsletterCreate(NewsletterBase):
    """Schema for creating a newsletter"""

    article_ids: Optional[List[int]] = []


class NewsletterUpdate(BaseModel):
    """Schema for updating a newsletter"""

    title: Optional[str] = None
    subject: Optional[str] = None
    template_id: Optional[int] = None
    template_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    scheduled_for: Optional[datetime] = None


class Newsletter(NewsletterBase):
    """Schema for newsletter responses"""

    id: int
    html_content: Optional[str] = None
    created_at: datetime
    sent_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    created_by: str
    updated_at: datetime

    class Config:
        from_attributes = True


class NewsletterList(BaseModel):
    """Schema for paginated newsletter list"""

    items: List[Newsletter]
    total: int
    page: int
    page_size: int
    total_pages: int


class NewsletterWithArticles(Newsletter):
    """Newsletter with article details"""

    article_ids: List[int]


class NewsletterSendRequest(BaseModel):
    """Schema for sending newsletters"""

    test_email: Optional[str] = None
    subscriber_ids: Optional[List[int]] = None  # If None, send to all active
