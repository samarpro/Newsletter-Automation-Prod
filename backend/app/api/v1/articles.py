"""
Article API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import math

from ...database import get_db
from ...services import ArticleService
from ...schemas import (
    Article,
    ArticleCreate,
    ArticleUpdate,
    ArticleList,
)

router = APIRouter()


@router.post("/", response_model=Article, status_code=201)
async def create_article(
    article_data: ArticleCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new article"""
    # Check if article with same link already exists
    existing = await ArticleService.get_by_link(db, article_data.link)
    if existing:
        raise HTTPException(status_code=400, detail="Article with this link already exists")

    article = await ArticleService.create(db, article_data)
    return article


@router.get("/{article_id}", response_model=Article)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get article by ID"""
    article = await ArticleService.get(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/", response_model=ArticleList)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List articles with pagination and filters"""
    skip = (page - 1) * page_size

    articles, total = await ArticleService.list(
        db,
        skip=skip,
        limit=page_size,
        status=status,
        search=search,
        category=category,
    )

    total_pages = math.ceil(total / page_size) if total > 0 else 0

    return ArticleList(
        items=articles,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.put("/{article_id}", response_model=Article)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an article"""
    article = await ArticleService.update(db, article_id, article_data)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete an article"""
    success = await ArticleService.delete(db, article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return None
