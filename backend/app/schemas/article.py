"""
Article Pydantic schemas
"""
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


class ArticleBase(BaseModel):
    """Base article schema"""

    title: str
    link: str
    categories: Optional[List[str]] = []
    published: Optional[datetime] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    ai_content: Optional[str] = None
    status: str = "draft"
    is_featured: bool = False


class ArticleCreate(ArticleBase):
    """Schema for creating an article"""

    pass


class ArticleUpdate(BaseModel):
    """Schema for updating an article"""

    title: Optional[str] = None
    link: Optional[str] = None
    categories: Optional[List[str]] = None
    published: Optional[datetime] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    ai_content: Optional[str] = None
    status: Optional[str] = None
    is_featured: Optional[bool] = None


class Article(ArticleBase):
    """Schema for article responses"""

    id: int
    scraped_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleList(BaseModel):
    """Schema for paginated article list"""

    items: List[Article]
    total: int
    page: int
    page_size: int
    total_pages: int
