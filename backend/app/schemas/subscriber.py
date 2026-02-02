"""
Subscriber Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class SubscriberBase(BaseModel):
    """Base subscriber schema"""

    email: EmailStr
    name: Optional[str] = None
    active: bool = True


class SubscriberCreate(SubscriberBase):
    """Schema for creating a subscriber"""

    pass


class SubscriberUpdate(BaseModel):
    """Schema for updating a subscriber"""

    name: Optional[str] = None
    active: Optional[bool] = None


class Subscriber(SubscriberBase):
    """Schema for subscriber responses"""

    id: int
    subscribed_at: datetime
    unsubscribed_at: Optional[datetime] = None
    unsubscribe_token: str
    email_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubscriberList(BaseModel):
    """Schema for paginated subscriber list"""

    items: List[Subscriber]
    total: int
    page: int
    page_size: int
    total_pages: int


class SubscriberImport(BaseModel):
    """Schema for bulk subscriber import"""

    subscribers: List[SubscriberCreate]
