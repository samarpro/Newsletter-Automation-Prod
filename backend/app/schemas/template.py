"""
Template Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class TemplateBase(BaseModel):
    """Base template schema"""

    name: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    template_json: Dict[str, Any]
    is_default: bool = False


class TemplateCreate(TemplateBase):
    """Schema for creating a template"""

    pass


class TemplateUpdate(BaseModel):
    """Schema for updating a template"""

    name: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    template_json: Optional[Dict[str, Any]] = None
    is_default: Optional[bool] = None


class Template(TemplateBase):
    """Schema for template responses"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TemplateList(BaseModel):
    """Schema for paginated template list"""

    items: List[Template]
    total: int
    page: int
    page_size: int
    total_pages: int
